#!/usr/bin/env python

import os
import sys
import time
import base
import psycopg2

if __name__ == '__main__':

    my_dir_name = os.path.dirname(os.path.realpath(__file__))

    config = base.config
    config.load_from_yaml(my_dir_name + f'/config/config.{os.getenv("ENVIRONMENT", "local")}.yaml')

    max_attempts = 30
    if config.conf['store']['type'] == 'redis':
        import redis

        for attempt in range(1, max_attempts):
            try:
                r = redis.Redis(host=config.conf['store']['host'],
                                port=config.conf['store']['port'])  # TODO: read params from config
            except Exception as e:
                print("waiting for redis server", e)
                time.sleep(attempt)
                continue

            break

        if attempt == max_attempts - 1:
            print("...error connecting to redis")
            sys.exit(128)

        print("...redis is ready")

    db_config = config.conf['db']

    if db_config['type'] == 'postgres':

        for attempt in range(1, 30):

            try:
                c = psycopg2.connect(database=db_config['database'],
                                     user=db_config['username'],
                                     password=db_config['password'],
                                     host=db_config['host'],
                                     port=db_config['port'])
            except:
                c = None

            if c and not c.closed:
                c.close()
                print(f"...database can accept connections {db_config['host']}:{db_config['port']}")
                sys.exit(0)

            print(
                f"waiting for postgres server {db_config['username']}@{db_config['host']}:{db_config['port']}/{db_config['database']} ...")
            time.sleep(attempt)

        sys.exit(127)
