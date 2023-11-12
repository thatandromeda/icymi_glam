from dataclasses import dataclass
import unittest
from unittest import mock

from dotenv import load_dotenv
import vcr

from run import client, run, standardize_args
from thresholds import get_threshold_from_name

load_dotenv()

my_vcr = vcr.VCR(
    cassette_library_dir='fixtures/cassettes',
    filter_headers=[('Authorization', 'XXXXXX'), 'min_id']
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


class TestInteractions(unittest.TestCase):
    @my_vcr.use_cassette('new_follows.yaml')
    @mock.patch.object(client, 'account_follow')
    def test_following_triggers_consent_request(self, mock_follow):
        run_for_test()
        mock_follow.assert_called_once()

# @my_vcr.use_cassette('new_follows_nobot.yaml')
# def test_following_with_nobot_does_not_trigger_consent_request(self):
#     assert False
#
# @my_vcr.use_cassette('new_follows_nobot.yaml')
# def test_following_with_nobot_does_not_trigger_follow(self):
#     assert False
#
# @my_vcr.use_cassette('new_follows_noindex.yaml')
# def test_following_with_noindex_does_not_trigger_consent_request(self):
#     assert False
#
# @my_vcr.use_cassette('new_follows_noindex.yaml')
# def test_following_with_noindex_does_not_trigger_follow(self):
#     assert False
#
# @my_vcr.use_cassette('consent.yaml')
# def test_consent_triggers_follow(self):
#     assert False
#
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
# @my_vcr.use_cassette('unfollow.yaml')
# def test_unfollow_triggers_unfollow(self):
#     assert False

if __name__ == '__main__':
    unittest.main()
