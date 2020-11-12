from base import http
import unittest

from tests.test_base_integration import SetUpTestAllServices


class TestIntegrationUsersAndContacts(SetUpTestAllServices):

    def test(self):
        self.api(None, 'GET', self.prefix('users') + '/about', expected_code=http.status.OK,
                 expected_result={'service': 'users'})
        self.api(None, 'GET', self.prefix('contacts') + '/about', expected_code=http.status.OK,
                 expected_result={'service': 'contacts'})
        self.api(None, 'GET', self.prefix('contacts') + '/test_ipc', expected_code=http.status.OK,
                 expected_result={'service': 'users'})

        if __name__ == '__main__':
            unittest.main()
