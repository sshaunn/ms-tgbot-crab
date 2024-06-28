import json


class Customer:
    def __init__(self, uid, firstname, lastname, tgid, register_time, is_member=False, is_whitelist=False, is_ban=False,
                 join_time=None, left_time=None):
        self.uid = uid
        self.firstname = firstname
        self.lastname = lastname
        self.tgid = tgid
        self.register_time = register_time
        self.is_member = is_member
        self.is_whitelist = is_whitelist
        self.is_ban = is_ban
        self.join_time = join_time
        self.left_time = left_time

    def set_membership(self, is_member):
        self.is_member = is_member

    def set_whitelist(self, is_whitelist):
        self.is_whitelist = is_whitelist

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
