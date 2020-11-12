from base import http
import unittest

from tests.test_base_integration import SetUpTestAllServices

THE_PASSWORD = 'SomePassword123!'

import lookup.user_permissions as perm


class TestIntegrationUsersAndContacts(SetUpTestAllServices):

    def test_about(self):
        self.api(None, 'GET', self.prefix('users') + '/about', expected_code=http.status.OK,
                 expected_result={'service': 'users'})
        self.api(None, 'GET', self.prefix('contacts') + '/about', expected_code=http.status.OK,
                 expected_result={'service': 'contacts'})
        self.api(None, 'GET', self.prefix('contacts') + '/test_ipc', expected_code=http.status.OK,
                 expected_result={'service': 'users'})

    def create_and_login(self, username, password, permissions):
        self.api(None, 'POST', self.prefix('users') + '/',
                 body={'user': {'username': username,
                                'password': password,
                                'permission_flags': permissions}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'}
                 )

        id_user = self.last_result['id']
        self.api(None, 'POST', self.prefix('users') + '/sessions',
                 {'username': username,
                  'password': password},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'})
        token = self.last_result['token']

        return id_user, token

    def test(self):
        self.id_admin, self.token_admin = self.create_and_login('admin', THE_PASSWORD, perm.ADMIN)
        self.id_admin, self.token_admin = self.create_and_login('user1', THE_PASSWORD, perm.USER)
        self.id_admin, self.token_admin = self.create_and_login('user2', THE_PASSWORD, perm.USER)


if __name__ == '__main__':
    unittest.main()
