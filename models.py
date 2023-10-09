from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scorers import Scorer


class ScoredPost:
    def __init__(self, post: dict):
        self.post = post

    @property
    def url(self) -> str:
        return self.post.url

    def get_home_url(self, mastodon_base_url: str) -> str:
        return f"{mastodon_base_url}/@{self.original_post.acct}/{self.original_post.id}"

    def get_score(self, scorer: Scorer) -> float:
        return scorer.score(self)

    @property
    def original_post(self):
        return self.post
