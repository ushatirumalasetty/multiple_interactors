from abc import ABC
from abc import abstractmethod

from gyaan.exceptions.exceptions import InvalidPostIds
from gyaan.interactors.presenters.dtos import DomainDetailsDTO, \
    DomainDetailsWithPosts
from gyaan.interactors.storages.dtos import CompletePostDetails


class PresenterInterface(ABC):

    @abstractmethod
    def raise_domain_does_not_exist_exception(self):
        pass

    @abstractmethod
    def raise_user_not_domain_member_exception(self):
        pass

    @abstractmethod
    def get_domain_details_response(
            self, domain_details_dto: DomainDetailsDTO):
        pass

    @abstractmethod
    def raise_exception_for_invalid_post_ids(self, err: InvalidPostIds):
        pass

    @abstractmethod
    def get_posts_response(self, post_details: CompletePostDetails):
        pass

    @abstractmethod
    def get_domain_posts_response(self, post_details: CompletePostDetails):
        pass

    @abstractmethod
    def get_domain_with_posts_response(
            self, domain_details_with_posts: DomainDetailsWithPosts
    ):
        pass
