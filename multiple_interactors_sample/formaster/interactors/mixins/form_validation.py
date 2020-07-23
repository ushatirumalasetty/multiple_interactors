"""
Created on 16/06/20

@author: revanth
"""
class FormClosed(Exception):
    pass


class FormValidationMixin:

    def validate_for_live_form(self, form_id: int):
        is_live = self.storage.get_form(form_id)
        if not is_live:
            raise FormClosed
