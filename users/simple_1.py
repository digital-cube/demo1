import base


@base.route("/")
class IndexHandler(base.Base):

    @base.api()
    async def get(self):
        return {'message': 'Hello World'}


if __name__ == "__main__":
    store = base.Store()

    config = base.config
    import os

    config.load_from_yaml(os.path.dirname(os.path.realpath(__file__)) + '/config/config.yaml')

    store.set('pera', 'zika')
    print(store.get('pera'))

    base.run()
