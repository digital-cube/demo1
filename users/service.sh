#!/bin/sh
./wait4db.py && cd db_migrations && alembic upgrade head && cd - &&  ./service.py
