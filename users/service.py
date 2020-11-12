#!/usr/bin/env python
import os
import base
import importlib

if __name__ == "__main__":
    config = base.config
    my_dir_name = os.path.dirname(os.path.realpath(__file__))
    config.load_from_yaml(my_dir_name + f'/config/config.{os.getenv("ENVIRONMENT", "local")}.yaml')

    importlib.import_module('api.users')
    importlib.import_module('lookup.user_permissions')

    base.run(debug=True)
