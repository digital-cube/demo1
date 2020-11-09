from base import orm


def create_db(db_config):
    import importlib

    importlib.import_module('service')
    _orm = orm.init_orm(db_config)
    _orm.clear_database()
    _orm.create_db_schema()


if __name__ == "__main__":
    import config

    create_db(db_config=config.db_config)
