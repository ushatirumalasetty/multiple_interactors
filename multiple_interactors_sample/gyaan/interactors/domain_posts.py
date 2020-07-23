"""
Created on 11/06/20

@author: revanth
"""
from gyaan.exceptions.exceptions import UserNotDomainMember, DomainDoesNotExist
from gyaan.interactors.presenters.presenter_interface import PresenterInterface
from gyaan.interactors.storages.storage_interface import StorageInterface


class DomainPostsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_domain_posts_wrapper(self, user_id: int, domain_id: int,
                                 offset: int, limit: int,
                                 presenter: PresenterInterface):

        try:
            return self._get_domain_posts_response(
                user_id=user_id,
                domain_id=domain_id,
                offset=offset,
                limit=limit,
                presenter=presenter
            )
        except UserNotDomainMember:
            presenter.raise_user_not_domain_member_exception()
        except DomainDoesNotExist:
            presenter.raise_domain_does_not_exist_exception()

    def _get_domain_posts_response(self, user_id: int, domain_id: int,
                                   offset: int, limit: int,
                                   presenter: PresenterInterface):
        posts_complete_details_dtos = self.get_domain_posts(
            user_id=user_id,
            domain_id=domain_id,
            offset=offset,
            limit=limit
        )
        return presenter.get_domain_posts_response(posts_complete_details_dtos)

    def get_domain_posts(self, user_id: int, domain_id: int,
                         offset: int, limit: int):
        self.storage.is_valid_domain_id(domain_id)

        is_user_domain_follower = self.storage.is_user_following_domain(
            user_id=user_id,
            domain_id=domain_id
        )

        if not is_user_domain_follower:
            raise UserNotDomainMember

        post_ids = self.storage.get_domain_post_ids(domain_id, offset, limit)

        from gyaan.interactors.get_posts import GetPosts
        get_post_interactor = GetPosts(storage=self.storage)

        return get_post_interactor.get_posts(post_ids=post_ids)
