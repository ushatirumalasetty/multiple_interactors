"""
Created on 11/06/20

@author: revanth
"""
from gyaan.exceptions.exceptions import UserNotDomainMember
from gyaan.interactors.presenters.dtos import DomainDetailsDTO
from gyaan.interactors.presenters.presenter_interface import PresenterInterface
from gyaan.interactors.storages.storage_interface import StorageInterface


class DomainDetailsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_domain_details_wrapper(self, domain_id: int, user_id: int,
                                   presenter: PresenterInterface) -> dict:
        from gyaan.exceptions.exceptions import DomainDoesNotExist
        try:
            return self._get_domain_details_response(
                domain_id=domain_id, user_id=user_id,
                presenter=presenter
            )
        except DomainDoesNotExist:
            presenter.raise_domain_does_not_exist_exception()
        except UserNotDomainMember:
            presenter.raise_user_not_domain_member_exception()

    def _get_domain_details_response(self, domain_id: int, user_id: int,
                                     presenter: PresenterInterface):
        domain_details_dto = self.get_domain_details(domain_id, user_id)
        response = presenter.get_domain_details_response(
            domain_details_dto)
        return response

    def get_domain_details(self, domain_id: int, user_id: int) -> \
            DomainDetailsDTO:

        domain_dto = self.storage.get_domain(domain_id)
        is_user_following = self.storage.is_user_following_domain(
            domain_id, user_id
        )
        if is_user_following:
            raise UserNotDomainMember

        domain_stats = self.storage.get_domain_stats(domain_id)
        domain_expert_ids = self.storage.get_domain_expert_ids(domain_id)
        domain_experts = self.storage.get_users_details(domain_expert_ids)

        is_user_domain_expert, domain_join_requests, requested_user_dtos = \
            self._get_domain_expert_details(
                user_id=user_id, domain_id=domain_id
            )
        response = DomainDetailsDTO(
            domain=domain_dto,
            domain_stats=domain_stats,
            domain_experts=domain_experts,
            user_id=user_id,
            is_user_domain_expert=is_user_domain_expert,
            join_requests=domain_join_requests,
            requested_users=requested_user_dtos
        )
        return response

    def _get_domain_expert_details(self, user_id: int, domain_id: int):
        is_user_domain_expert = self.storage.is_user_domain_expert(
            domain_id, user_id
        )
        domain_join_requests = []
        requested_user_dtos = []

        if is_user_domain_expert:
            domain_join_requests = self.storage.get_domain_join_requests(
                domain_id
            )
        if domain_join_requests:
            requested_user_dtos = self.storage.get_users_details(
                user_ids=[dto.user_id for dto in domain_join_requests]
            )
        return is_user_domain_expert, domain_join_requests, requested_user_dtos
