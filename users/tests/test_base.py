from base import test
import unittest
import importlib

import os

current_file_folder = os.path.dirname(os.path.realpath(__file__))


# from unittest.mock import patch


class SetUpTestUserServiceBase(test.BaseTest):

    def prefix(self):
        return '/api/users'

    def setUp(self):
        from base import registry, Base, orm, app, config
        config.load_from_yaml(os.path.dirname(os.path.realpath(__file__)) + f'/../config/config.{os.getenv("ENVIRONMENT", "local")}.yaml')
        config.conf['db']['database'] = f"test_{config.conf['db']['database']}"

        # registry.register({'name': 'users',
        #                    'prefix': '/api/users',
        #                    'port': None,
        #                    # "db": _config.db_config
        #                    })

        importlib.import_module('orm.models')
        registry.test = True

        # db_config = registry.db('users')

        orm = orm.init_orm(config.conf['db'])

        orm.clear_database()
        orm.create_db_schema()

        importlib.import_module('api.users')
        self.my_app = app.make_app(debug=True)

        super().setUp()
        registry.test_port = self.get_http_port()


if __name__ == '__main__':
    unittest.main()
