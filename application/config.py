import os, base

port = os.getenv('APP_PORT', 9000)

db_config = {
    "type": 'postgres',
    "port": os.getenv('POSTGRES_PORT', 5432),
    "host": os.getenv('POSTGRES_HOST', 'localhost'),
    "username": os.getenv('POSTGRES_USER', 'demo'),
    "password": os.getenv('POSTGRES_PASSWORD', 'demo'),
    "database": os.getenv('POSTGRES_DB', 'application')
}

base.registry.register({
    "name": "users",
    "port": port,
    "prefix": "/api/users",
    "db":
        db_config
})
