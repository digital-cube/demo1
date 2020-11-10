import base


@base.route("/")
class IndexHandler(base.Base):

    @base.api()
    async def get(self):
        return {'message': 'Hello World'}


if __name__ == "__main__":
    base.run()
