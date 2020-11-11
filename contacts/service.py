#!/usr/bin/env python
import base
import os

if __name__ == "__main__":

    import api.contacts

    my_dir_name = os.path.dirname(os.path.realpath(__file__))

    config = base.config
    config.load_from_yaml(my_dir_name + f'/config/config.{os.getenv("ENVIRONMENT", "local")}.yaml')

    # import lookup.permissions as perm

    # print("ADMIN2", perm.permission['ADMIN'])
    # print("USER", perm.USER)

    base.run(debug=True, port=config.conf['port'])
