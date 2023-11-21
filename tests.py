from dataclasses import dataclass
import unittest
from unittest import mock

from dotenv import load_dotenv
from mastodon.utility import AttribAccessDict
import vcr

from run import client, run, standardize_args
from thresholds import get_threshold_from_name

load_dotenv()

my_vcr = vcr.VCR(
    cassette_library_dir='fixtures/cassettes',
    filter_headers=[('Authorization', 'XXXXXX')],
    filter_query_parameters=['min_id']
)

def run_for_test():
    @dataclass
    class BotArgs:
        hours: int
        scorer: str
        threshold: str

    args = BotArgs(
        hours=12,
        scorer='SimpleWeighted',
        threshold='lax'
    )

    run(*standardize_args(args))

follow_list = [
    AttribAccessDict({'id': 109774209386827066,
     'username': 'thatandromeda',
     'acct': 'thatandromeda@ohai.social',
     'display_name': 'Andromeda Yelton',
     'note': '<p>Hi! I’m the same thatandromeda you may know from elsewhere online. Studied <a href="https://ohai.social/tags/math" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>math</span></a>, taught <a href="https://ohai.social/tags/Latin" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>Latin</span></a> to middle school boys, trained as a <a href="https://ohai.social/tags/librarian" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>librarian</span></a>, ended up writing <a href="https://ohai.social/tags/software" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>software</span></a> for a variety of libraries and adjacent organizations. Things I’ve obsessed over include nonprofit governance, <a href="https://ohai.social/tags/weightlifting" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>weightlifting</span></a>, <a href="https://ohai.social/tags/knitting" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>knitting</span></a>, <a href="https://ohai.social/tags/singing" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>singing</span></a>, my cats, and <a href="https://ohai.social/tags/planes" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>planes</span></a> (working slowly on my pilot’s license). Married, mom to a teenager, extremely online for a long time. <a href="https://ohai.social/tags/introduction" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>introduction</span></a></p>'
    })
]

follow_list_nobot = [
    AttribAccessDict({'id': 109774209386827066,
     'username': 'thatandromeda',
     'acct': 'thatandromeda@ohai.social',
     'display_name': 'Andromeda Yelton',
     'note': '<p>Hi! I’m the same thatandromeda you may know from elsewhere online. Studied <a href="https://ohai.social/tags/math" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>math</span></a>, taught <a href="https://ohai.social/tags/Latin" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>Latin</span></a> to middle school boys, trained as a <a href="https://ohai.social/tags/librarian" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>librarian</span></a>, ended up writing <a href="https://ohai.social/tags/software" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>software</span></a> for a variety of libraries and adjacent organizations. Things I’ve obsessed over include nonprofit governance, <a href="https://ohai.social/tags/weightlifting" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>weightlifting</span></a>, <a href="https://ohai.social/tags/knitting" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>knitting</span></a>, <a href="https://ohai.social/tags/singing" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>singing</span></a>, my cats, and <a href="https://ohai.social/tags/planes" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>planes</span></a> (working slowly on my pilot’s license). Married, mom to a teenager, extremely online for a long time. <a href="https://ohai.social/tags/introduction" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>introduction</span></a> <a href="https://ohai.social/tags/nobot" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>nobot</span></a></p>'
    })
]

follow_list_noindex = [
    AttribAccessDict({'id': 109774209386827066,
     'username': 'thatandromeda',
     'acct': 'thatandromeda@ohai.social',
     'display_name': 'Andromeda Yelton',
     'note': '<p>Hi! I’m the same thatandromeda you may know from elsewhere online. Studied <a href="https://ohai.social/tags/math" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>math</span></a>, taught <a href="https://ohai.social/tags/Latin" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>Latin</span></a> to middle school boys, trained as a <a href="https://ohai.social/tags/librarian" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>librarian</span></a>, ended up writing <a href="https://ohai.social/tags/software" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>software</span></a> for a variety of libraries and adjacent organizations. Things I’ve obsessed over include nonprofit governance, <a href="https://ohai.social/tags/weightlifting" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>weightlifting</span></a>, <a href="https://ohai.social/tags/knitting" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>knitting</span></a>, <a href="https://ohai.social/tags/singing" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>singing</span></a>, my cats, and <a href="https://ohai.social/tags/planes" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>planes</span></a> (working slowly on my pilot’s license). Married, mom to a teenager, extremely online for a long time. <a href="https://ohai.social/tags/introduction" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>introduction</span></a> <a href="https://ohai.social/tags/noindex" class="mention hashtag" rel="nofollow noopener noreferrer" target="_blank">#<span>noindex</span></a></p>'
    })
]

@mock.patch('run.client.account_following', mock.MagicMock(return_value=[]))
@mock.patch('run.client.account_followers', mock.MagicMock(return_value=follow_list))
class TestFollow(unittest.TestCase):
    @my_vcr.use_cassette('new_follows.yaml')
    @mock.patch.object(client, 'status_post')
    # Don't do anything after the initial post.
    @mock.patch('run.check_for_user_consents')
    def test_following_triggers_consent_request(self, mock_post, _mock_consents):
        run_for_test()
        mock_post.assert_called_once()


@mock.patch('run.client.account_following', mock.MagicMock(return_value=follow_list))
@mock.patch('run.client.account_followers', mock.MagicMock(return_value=[]))
class TestUnfollow(unittest.TestCase):
    @my_vcr.use_cassette('unfollow.yaml')
    @mock.patch.object(client, 'account_unfollow')
    def test_unfollow_triggers_unfollow(self, mock_unfollow):
        run_for_test()
        mock_unfollow.assert_called_once()


@mock.patch('run.client.account_following', mock.MagicMock(return_value=[]))
@mock.patch('run.client.account_followers', mock.MagicMock(return_value=follow_list_nobot))
class TestInteractionsNobot(unittest.TestCase):
    @my_vcr.use_cassette('new_follows_nobot.yaml')
    @mock.patch.object(client, 'status_post')
    def test_following_with_nobot_does_not_trigger_consent_request(self, mock_post):
        run_for_test()
        mock_post.assert_not_called()

    @my_vcr.use_cassette('new_follows_nobot.yaml')
    @mock.patch.object(client, 'account_follow')
    def test_following_with_nobot_does_not_trigger_follow(self, mock_follow):
        run_for_test()
        mock_follow.assert_not_called()


@mock.patch('run.client.account_following', mock.MagicMock(return_value=[]))
@mock.patch('run.client.account_followers', mock.MagicMock(return_value=follow_list_noindex))
class TestInteractionsNoindex(unittest.TestCase):
    @my_vcr.use_cassette('new_follows_noindex.yaml')
    @mock.patch.object(client, 'status_post')
    def test_following_with_noindex_does_not_trigger_consent_request(self, mock_post):
        run_for_test()
        mock_post.assert_not_called()

    @my_vcr.use_cassette('new_follows_noindex.yaml')
    @mock.patch.object(client, 'account_follow')
    def test_following_with_noindex_does_not_trigger_follow(self, mock_follow):
        run_for_test()
        mock_follow.assert_not_called()


@mock.patch('run.client.account_following', mock.MagicMock(return_value=follow_list))
@mock.patch('run.client.account_followers', mock.MagicMock(return_value=follow_list))
class TestInteractionsWithMutual(unittest.TestCase):
    @my_vcr.use_cassette('consent.yaml')
    @mock.patch.object(client, 'status_post')
    def test_consent_triggers_follow(self, mock_post):
        run_for_test()
        assert(mock_post.call_count == 2)

# @my_vcr.use_cassette('boost.yaml')
# def test_popular_post_triggers_boost(self):
#     assert False
#
# @my_vcr.use_cassette('boost_nobot.yaml')
# def test_popular_post_with_nobot_does_not_trigger_boost(self):
#     assert False
#
# @my_vcr.use_cassette('boost_noindex.yaml')
# def test_popular_post_with_noindex_does_not_trigger_boost(self):
#     assert False
#

if __name__ == '__main__':
    unittest.main()
