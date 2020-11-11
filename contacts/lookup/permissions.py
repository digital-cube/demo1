
permission = {}

def init():

    # print("LOADING PERMISSIONS")

    import sys
    import base
    import json
    thismodule = sys.modules[__name__]

    from tornado.httpclient import HTTPClient

    # uri = 'http://localhost:9000/api/users/permissions'
    uri = 'http://users/api/users/permissions'

    http_client = HTTPClient()

    result = http_client.fetch(uri, method='GET')
    if result:
        permissions = json.loads(result.body.decode('utf-8'))
        # print("RESULT",permissions)

        for perm in permissions:
            # print('perm',perm)
            setattr(thismodule, perm, permissions[perm])

        permission.update(permissions)


# init()
