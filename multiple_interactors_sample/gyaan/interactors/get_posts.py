from typing import List

from gyaan.exceptions.exceptions import InvalidPostIds
from gyaan.interactors.presenters.presenter_interface import PresenterInterface
from gyaan.interactors.storages.dtos import CompletePostDetails
from gyaan.interactors.storages.storage_interface import StorageInterface


class GetPosts:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_posts_wrapper(self, post_ids: List[int],
                          presenter: PresenterInterface):
        try:
            return self._prepare_posts_response(
                post_ids=post_ids,
                presenter=presenter
            )
        except InvalidPostIds as err:
            presenter.raise_exception_for_invalid_post_ids(err)

    def _prepare_posts_response(self, post_ids: List[int],
                                presenter: PresenterInterface):
        completed_post_details = self.get_posts(post_ids=post_ids)
        return presenter.get_posts_response(completed_post_details)

    def get_posts(self, post_ids: List[int]):
        unique_post_ids = self._get_unique_post_ids(post_ids)

        self._validate_post_ids(post_ids=unique_post_ids)

        post_dtos = self.storage.get_post_details(
            post_ids=post_ids
        )

        post_tag_details = self.storage.get_post_tags(post_ids=post_ids)

        post_reaction_counts = self.storage.get_post_reactions_count(
            post_ids=post_ids
        )
        posts_comment_counts = self.storage.get_post_comments_count(
            post_ids=post_ids
        )

        comment_ids = self._get_latest_comment_ids(post_ids=post_ids)

        comment_reaction_counts = \
            self.storage.get_comment_reactions_count(comment_ids=comment_ids)

        comment_replies_counts = \
            self.storage.get_comment_replies_count(comment_ids=comment_ids)

        comment_dtos = self.storage.get_comment_details(
            comment_ids=comment_ids
        )

        user_ids = [post_dto.posted_by_id for post_dto in post_dtos]
        user_ids += [
            comment_dto.commented_by_id for comment_dto in comment_dtos
        ]

        user_dtos = self.storage.get_users_details(user_ids=user_ids)

        return CompletePostDetails(
            post_dtos=post_dtos,
            post_reaction_counts=post_reaction_counts,
            comment_counts=posts_comment_counts,
            comment_reaction_counts=comment_reaction_counts,
            reply_counts=comment_replies_counts,
            comment_dtos=comment_dtos,
            post_tag_ids=post_tag_details.post_tag_ids,
            tags=post_tag_details.tags,
            users_dtos=user_dtos
        )

    def _get_latest_comment_ids(self, post_ids):
        comment_ids = []
        for post_id in post_ids:
            comment_ids += self.storage.get_latest_comment_ids(
                post_id=post_id, no_of_comments=2
            )
        return comment_ids

    @staticmethod
    def _get_unique_post_ids(post_ids):
        return list(set(post_ids))

    def _validate_post_ids(self, post_ids):
        valid_post_ids = self.storage.get_valid_post_ids(post_ids)

        invalid_post_ids = [
            post_id
            for post_id in post_ids if post_id not in valid_post_ids
        ]
        if invalid_post_ids:
            raise InvalidPostIds(invalid_post_ids=invalid_post_ids)
        return
