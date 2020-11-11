
USER = 2 ** 0
ADMIN = 2 ** 1





def all_permissions():
    import inspect

    my_name = inspect.stack()[0][3]

    permissions = {}

    for perm in globals():
        if (perm[:2] == perm[-2:] and perm[:2] == '__') or perm == my_name:
            continue
        permissions[perm] = eval(perm)

    return permissions


