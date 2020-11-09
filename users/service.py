#!/usr/bin/env python
import base

if __name__ == "__main__":
    import api.users

    import config
    import _config

    _config.db_config = config.db_config

    base.registry.register({
        "name": "users",
        "port": config.port,
        "prefix": base.route.get('prefix'),
        "db":
            config.db_config
    })

    base.run(port=config.port,
             debug=True)
