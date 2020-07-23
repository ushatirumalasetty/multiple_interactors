class DomainDoesNotExist(Exception):
    pass


class UserNotDomainMember(Exception):
    pass


class InvalidPostIds(Exception):
    def __init__(self, invalid_post_ids):
        self.invalid_post_ids = invalid_post_ids
