from base import test, http
import unittest
import importlib

import os

current_file_folder = os.path.dirname(os.path.realpath(__file__))


class SetUpTestUserServiceBase(test.BaseTest):

    def prefix(self, service):

        if service == 'users':
            return '/api/users'
        if service == 'contacts':
            return '/api/contacts'

    def setUp(self):
        from base import registry, orm, app, config
        config.load_from_yaml(
            os.path.dirname(os.path.realpath(__file__)) + f'/../config.singleservice.yaml')

        config.conf['db']['database'] = f"test_{config.conf['db']['database']}"

        importlib.import_module('orm.models')

        registry.test = True

        orm = orm.init_orm(config.conf['db'])

        orm.clear_database()
        orm.create_db_schema()

        importlib.import_module('users.api.users')
        importlib.import_module('contacts.api.contacts')

        self.my_app = app.make_app(debug=True)

        super().setUp()
        registry.test_port = self.get_http_port()

    def test(self):

        self.api(None, 'GET', self.prefix('users') + '/about', expected_code=http.status.OK,
                 expected_result={'service': 'users'})
        self.api(None, 'GET', self.prefix('contacts') + '/about', expected_code=http.status.OK,
                 expected_result={'service': 'contacts'})
        self.api(None, 'GET', self.prefix('contacts')+'/test_ipc')
        self.show_last_result()


if __name__ == '__main__':
    unittest.main()
