from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from mastodon import Mastodon

from api import fetch_posts_and_boosts
from scorers import get_scorers, Scorer
from thresholds import get_threshold_from_name, get_thresholds

if TYPE_CHECKING:
    from scorers import Scorer
    from thresholds import Threshold

# TODO:
# For automated testing:
    # Follow the bot and run script
    # Confirm that you get a request for consent
    # Send consent and run script
    # Confirm that you get followed
    # Rerun with -n 24
    # Check for boost
    # Unfollow and run script
    # Confirm that you are unfollowed
    # Add #nobot to profile
    # Follow and run script
    # Confirm that you are not followed or mentioned
    # Remove #nobot
# Deal with github deploy
# Make info page (github pages)
#  And link from profile
# Deal with clever database stuff post-launch

load_dotenv()

# Chad Nelson quite rightly points out that I can use git as a data store,
# because...duh. (oooh, jsonata)
# might wanna make it a private repo in that case, and then think about if I
# can still run the action. (Orrrr: you can encrypt it, using a github secret.)
# What are the implications of follow/unfollow? If people follow/unfollow/
# refollow you, do you get that in sequence?
def fetch_content(
    hours: int,
    scorer: Scorer,
    threshold: Threshold,
    client: Mastodon,
    mastodon_username: str
) -> list[dict]:
    # 1. Fetch all the posts and boosts from our home timeline that we haven't interacted with
    posts, boosts = fetch_posts_and_boosts(hours, client, mastodon_username)

    # 2. Score them, and return those that meet our threshold
    threshold_posts = threshold.posts_meeting_criteria(posts, scorer)
    threshold_boosts = threshold.posts_meeting_criteria(boosts, scorer)

    return threshold_posts, threshold_boosts


def acknowledge_consent(client, mention):
    account = mention.account
    client.account_follow(account.id)
    client.status_post(
        status=f"👍 Thanks, @{account.acct}! I'll read your timeline now.",
        visibility='direct',
        idempotency_key=f"do_not_spam_ack_{account.acct}"
    )


def check_for_user_consents(client, followers):
    mentions = client.notifications(mentions_only=True)
    for mention in mentions:
        print("______Checking notification for follow status")
        if not mention.account in followers:
            continue

        print("______Checking for consents")
        if not check_profile_consent(mention.account):
            continue

        post = mention.status.content
        if 'i consent' in post.lower():
            acknowledge_consent(client, mention)


def check_profile_consent(account):
    # TODO: check db/cache first? periodically expire db?
    note_text = BeautifulSoup(account.note, 'html.parser').text
    if any([
        '#nobot' in note_text,
        '#noindex' in note_text,
    ]):
        return False

    return True


# Are we gonna need a db at this point? Or not, because we get account['note']
# along with the post, so we don't need a separate call? And we maintain state
# in the follow graph?
def check_post_consent(client, post):
    print("____Checking post visibility")
    if not post.visibility == 'public':
        return None

    print("____Checking for profile consent")
    if not check_profile_consent(post.account):
        return None

    return post


# Also run this on the cron/as part of run()
# https://mastodonpy.readthedocs.io/en/stable/06_accounts.html#id1
def handle_follow_asymmetry(client):
    print("____Getting follow{ing,ers}")
    my_id = client.me()['id']
    following = client.account_following(my_id)
    followers = client.account_followers(my_id)
    print("__Checking unfollows")
    check_for_unfollows(client, following, followers)
    print("__Checking new follows")
    check_for_new_follows(client, following, followers)
    print("__Checking user consents")
    check_for_user_consents(client, followers)


def get_id_diff(include, exclude):
    included_ids = [account.id for account in include]
    excluded_ids = [account.id for account in exclude]
    return set(included_ids) - set(excluded_ids)

# If you are following people who are no longer following you, unfollow
# and notify.
def check_for_unfollows(client, following, followers):
    unfollows = get_id_diff(following, followers)

    for account in following:
        if account.id not in unfollows:
            continue

        print("____Unfollowing")
        client.account_unfollow(account.id)
        client.status_post(
            status=(f"@{account.acct} It looks like you no longer follow "
                     "me. Sorry to see you go, but I respect your choice! I "
                     "won't watch your timeline any more. I may boost your "
                     "public posts when they have been boosted by other people "
                     "I follow. If you don't want that, add #nobot to your "
                     "profile; I and many other bots respect that setting."
                   ),
            visibility='direct',
            idempotency_key=f"do_not_spam_unfollow_{account.acct}"
        )


# Send a friendly explanatory post to new followers.
def check_for_new_follows(client, following, followers):
    new_follows = get_id_diff(followers, following)

    for account in followers:
        if account.id not in new_follows:
            continue

        print("____Checking new follower profile consent")
        if not check_profile_consent(account):
            # TODO should I thank them for the follow and tell them I won't
            # follow or read their account? Or should I just not interact with
            # them at all?
            continue

        print("____Greeting new follower")
        client.status_post(
            status=(f"👋 Hi, @{account.acct}! Thanks for following me. "
                     "I aggregate things that GLAM people are talking about, "
                     "in case you missed it. You can help me get better at it "
                     "by letting me read your timeline; details in my bio. To "
                     "permit this, send me a message that includes my username "
                     "and the phrase 'I consent'."
                   ),
            visibility='direct',
            idempotency_key=f"do_not_spam_follow_{account.acct}"
        )


def run(
    hours: int,
    scorer: Scorer,
    threshold: Threshold,
    mastodon_token: str,
    mastodon_base_url: str,
    mastodon_username: str
) -> None:

    print("__Initializing client")
    client = Mastodon(
        access_token=mastodon_token,
        api_base_url=mastodon_base_url,
    )

    print("__Handling follow asymmetry")
    handle_follow_asymmetry(client)

    print("__Fetching popular posts")
    # Is this just people we follow? Or does it include messages which @ us?
    # If the latter, we don't need a db. If the former, maybe we do???
    # This is just home timeline. We will need a separate client.notifications
    # thing to do the consent logic, which will then need to be separated out of
    # check_post_consent.
    threshold_posts, threshold_boosts = fetch_content(
        hours, scorer, threshold, client, mastodon_username
    )

    print("__Checking post consent")
    consented_posts = [
        check_post_consent(client, post.original_post)
        for post in threshold_posts
    ]
    consented_boosts = [
        check_post_consent(client, boost.original_post)
        for boost in threshold_boosts
    ]

    print("__Reblogging")
    [client.status_reblog(post) for post in consented_posts if post]
    [client.status_reblog(boost) for boost in consented_boosts if boost]


if __name__ == "__main__":
    print("Getting scorers and thresholds")
    scorers = get_scorers()
    thresholds = get_thresholds()

    print("Parsing args")
    arg_parser = argparse.ArgumentParser(
        prog="mastodon_digest",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument(
        "-n",
        choices=range(1, 25),
        default=12,
        dest="hours",
        help="The number of hours to include in the Mastodon Digest",
        type=int,
    )
    arg_parser.add_argument(
        "-s",
        choices=list(scorers.keys()),
        default="SimpleWeighted",
        dest="scorer",
        help="""Which post scoring criteria to use.
            Simple scorers take a geometric mean of boosts and favs.
            Extended scorers include reply counts in the geometric mean.
            Weighted scorers multiply the score by an inverse square root
            of the author's followers, to reduce the influence of large accounts.
        """,
    )
    arg_parser.add_argument(
        "-t",
        choices=list(thresholds.keys()),
        default="normal",
        dest="threshold",
        help="""Which post threshold criteria to use.
            lax = 90th percentile,
            normal = 95th percentile,
            strict = 98th percentile
        """,
    )
    args = arg_parser.parse_args()

    print("Fetching env")
    mastodon_token = os.getenv("MASTODON_TOKEN")
    mastodon_base_url = os.getenv("MASTODON_BASE_URL")
    mastodon_username = os.getenv("MASTODON_USERNAME")

    if not mastodon_token:
        sys.exit("Missing environment variable: MASTODON_TOKEN")
    if not mastodon_base_url:
        sys.exit("Missing environment variable: MASTODON_BASE_URL")
    if not mastodon_username:
        sys.exit("Missing environment variable: MASTODON_USERNAME")

    print("Running the good stuff")
    run(
        args.hours,
        scorers[args.scorer](),
        get_threshold_from_name(args.threshold),
        mastodon_token,
        mastodon_base_url,
        mastodon_username
    )
