from base import test
import unittest

import os

current_file_folder = os.path.dirname(os.path.realpath(__file__))


class Test1(test.BaseTest):

    def setUp(self):
        import redis
        r = redis.Redis()
        r.flushall()

        from base import registry, Base, orm, app

        registry.register({'name': 'users',
                           'prefix': '/api/users',
                           'port': None,
                           "db":
                               {
                                   "type": "postgresql",
                                   "port": "5432",
                                   "host": "localhost",
                                   "username": "demo",
                                   "password": "123",
                                   "database": "test_demo"
                               }})

        import service

        self.my_app = app.make_app()

        registry.test = True

        db_config = registry.db('users')
        orm = orm.init_orm(db_config)
        orm.clear_database()
        orm.create_db_schema()

        super().setUp()
        registry.test_port = self.get_http_port()

    def test(self):
        self.api(None, "GET", "/api/users")
        self.show_last_result()


if __name__ == '__main__':
    unittest.main()
