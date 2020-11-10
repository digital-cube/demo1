#!/usr/bin/env python
import base

if __name__ == "__main__":
    import api.users

    # import config
    # import _config

    # _config.db_config = config.db_config

    # base.config.load_from_dict({
    #     "name": "users",
    #     "port": config.port,
    #     "prefix": base.route.get('prefix'),
    #     "db":
    #         config.db_config
    # })

    import os
    full_path = os.path.realpath(__file__)
    my_dir_name = os.path.dirname(full_path)

    config = base.config
    config.load_from_yaml(my_dir_name + '/config/config.yaml')

    base.run(debug=True)
