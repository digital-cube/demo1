#!/usr/bin/env python

import sys
import time
import psycopg2

if __name__=='__main__':

    from config import db_config

    if db_config['type']=='postgres':

        for attempt in range(1,30):

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
                print('...database can accept connections')
                sys.exit(0)

            print('waiting for postgres server ...')
            time.sleep(attempt)
        
        sys.exit(127)