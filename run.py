from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from mastodon import Mastodon

from api import fetch_posts_and_boosts
from scorers import get_scorers
from thresholds import get_threshold_from_name, get_thresholds
from formatters import format_posts

if TYPE_CHECKING:
    from scorers import Scorer
    from thresholds import Threshold

load_dotenv()

def fetch_content(
    hours: int,
    scorer: Scorer,
    threshold: Threshold,
    client: Mastodon,
    mastodon_username: str
) -> list[dict]:
    print(f"Building digest from the past {hours} hours...")

    # 1. Fetch all the posts and boosts from our home timeline that we haven't interacted with
    posts, boosts = fetch_posts_and_boosts(hours, client, mastodon_username)

    # 2. Score them, and return those that meet our threshold
    threshold_posts = format_posts(
        threshold.posts_meeting_criteria(posts, scorer),
        mastodon_base_url)
    threshold_boosts = format_posts(
        threshold.posts_meeting_criteria(boosts, scorer),
        mastodon_base_url)

    return threshold_posts, threshold_boosts


def run(
    hours: int,
    scorer: Scorer,
    threshold: Threshold,
    mastodon_token: str,
    mastodon_base_url: str,
    mastodon_username: str
) -> None:

    client = Mastodon(
        access_token=mastodon_token,
        api_base_url=mastodon_base_url,
    )

    threshold_posts, threshold_boosts = fetch_content(
        hours, scorer, threshold, client, mastodon_username
    )

    [client.status_reblog(post) for post in threshold_posts]
    [client.status_reblog(post) for boost in threshold_boosts]


if __name__ == "__main__":
    scorers = get_scorers()
    thresholds = get_thresholds()

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

    mastodon_token = os.getenv("MASTODON_TOKEN")
    mastodon_base_url = os.getenv("MASTODON_BASE_URL")
    mastodon_username = os.getenv("MASTODON_USERNAME")

    if not mastodon_token:
        sys.exit("Missing environment variable: MASTODON_TOKEN")
    if not mastodon_base_url:
        sys.exit("Missing environment variable: MASTODON_BASE_URL")
    if not mastodon_username:
        sys.exit("Missing environment variable: MASTODON_USERNAME")

    run(
        args.hours,
        scorers[args.scorer](),
        get_threshold_from_name(args.threshold),
        mastodon_token,
        mastodon_base_url,
        mastodon_username
    )
