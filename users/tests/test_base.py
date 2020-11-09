from base import test
import unittest
import importlib

import os

current_file_folder = os.path.dirname(os.path.realpath(__file__))


class SetUpTestUserServiceBase(test.BaseTest):

    def prefix(self):
        return '/api/users'

    def setUp(self):
        import redis
        r = redis.Redis()
        r.flushall()

        from base import registry, Base, orm, app

        import config
        import _config

        # print('RRR config.db_config', config.db_config['database'])

        _config.db_config = config.db_config

        # _config.db_config['database'] = 'test_' + config.db_config['database']
        _config.db_config['database'] = 'test_demo_users' # ?!!?!

        # print('RRR2 _config.db_config', _config.db_config['database'])


        registry.register({'name': 'users',
                           'prefix': '/api/users',
                           'port': None,
                           # "db": _config.db_config
                           })

        importlib.import_module('orm.models')

        registry.test = True

        # db_config = registry.db('users')

        # print("INICIRAM ORM", _config.db_config['database'])
        orm = orm.init_orm(_config.db_config)

        # print("BRISEM CELU BAZU")
        orm.clear_database()

        # print("KREIRAM TABELE")
        orm.create_db_schema()

        importlib.import_module('api.users')
        self.my_app = app.make_app(debug=True)

        super().setUp()
        registry.test_port = self.get_http_port()

        # app.route.print_all_routes()


if __name__ == '__main__':
    unittest.main()
