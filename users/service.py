#!/usr/bin/env python
import base

if __name__ == "__main__":
    import api.users

    import os
    full_path = os.path.realpath(__file__)
    my_dir_name = os.path.dirname(full_path)

    config = base.config
    config.load_from_yaml(my_dir_name + '/config/config.yaml')

    base.run(debug=True)
