from . import auth as syn


class Core(object):
    def __init__(self, ip_address, port, username, password, secure=False, cert_verify=False, dsm_version=2):

        self.session = syn.Authentication(ip_address, port, username, password, secure, cert_verify, dsm_version)

        self.session.login('Core')
        self.session.get_api_list('Core')
        self.session.get_api_list()

        self.request_data = self.session.request_data
        self.core_list = self.session.app_api_list
        self.gen_list = self.session.full_api_list
        self._sid = self.session.sid
        self.base_url = self.session.base_url

        print('You are now logged in!')

    def logout(self):
        self.session.logout('Core')
