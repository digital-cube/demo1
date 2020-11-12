import os
import base
import importlib

if __name__ == "__main__":
    my_dir_name = os.path.dirname(os.path.realpath(__file__))
    base.config.load_from_yaml(my_dir_name + f'/config.singleservice.yaml')

    importlib.import_module('users.api.users')
    importlib.import_module('lookup.user_permissions')
    importlib.import_module('contacts.api.contacts')

    base.run(debug=True)
