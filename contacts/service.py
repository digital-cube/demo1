#!/usr/bin/env python
import base
import os

if __name__ == "__main__":

    import api.contacts

    my_dir_name = os.path.dirname(os.path.realpath(__file__))

    config = base.config
    config.load_from_yaml(my_dir_name + f'/config/config.{os.getenv("ENVIRONMENT", "local")}.yaml')

    base.run(debug=True)
