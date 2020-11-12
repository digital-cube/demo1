from base import test, http, config, registry, app
import importlib

import os

current_file_folder = os.path.dirname(os.path.realpath(__file__))


class SetUpTestAllServices(test.BaseTest):

    def prefix(self, service):
        return config.conf['services'][service]['prefix']

    def setUp(self):
        from base import orm
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

        from base import store
        with open(os.path.dirname(os.path.realpath(__file__)) + '/../users/keys/jwt.public_key') as pubkey:
            store.set('users_service_public_key', pubkey.read())

        config.load_private_key(os.path.dirname(os.path.realpath(__file__)) + '/../users/keys/jwt.private_key')

        super().setUp()
        registry.test_port = self.get_http_port()

