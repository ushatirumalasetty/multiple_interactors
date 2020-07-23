"""
Created on 16/06/20

@author: revanth
"""
from abc import abstractmethod

from formaster.interactors.mixins.form_validation import FormValidationMixin


class BaseSubmitFormResponseInteractor(FormValidationMixin):

    def __init__(self, storage: StorageInterface, question_id: int,
                 form_id: int, user_id: int):
        self.storage = storage
        self.question_id = question_id
        self.form_id = form_id
        self.user_id = user_id

    def submit_form_response_wrapper(self, presenter: PresenterInterface):
        try:
            user_response_id = self.submit_form_response()
            return presenter.submit_form_response_return(user_response_id)
        except FormDoesNotExist:
            presenter.raise_form_does_not_exist_exception()
        except FormClosed:
            presenter.raise_form_closed_exception()
        except QuestionDoesNotBelongToForm:
            presenter.raise_question_does_not_belong_to_form_exception()
        except InvalidUserResponseSubmit:
            presenter.raise_invalid_user_response_submitted()

    def submit_form_response(self):
        self.validate_for_live_form(self.form_id)
        self.storage.validate_question_id_with_form(
            self.question_id, self.form_id)

        self._validate_user_response()
        user_response_id = self._create_user_response()

        return user_response_id

    @abstractmethod
    def _validate_user_response(self):
        pass

    @abstractmethod
    def _create_user_response(self) -> int:
        pass
