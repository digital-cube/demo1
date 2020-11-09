import unittest
from base import http
from tests.test_base import SetUpTestUserServiceBase

THE_PASSWORD = 'SomePassword123!'

import lookup.user_permissions as perm


class TestUsersCreatingAdminUser(SetUpTestUserServiceBase):

    def test_unauthorized_user_tries_to_fetch_list_of_all_users(self):
        self.api(None, 'GET', self.prefix() + '/', expected_code=http.status.UNAUTHORIZED)
        self.api('INVALIDTOKEN', 'GET', self.prefix() + '/', expected_code=http.status.UNAUTHORIZED)

    def test_tries_to_initially_register_admin_user_after_non_admin_users_has_been_registered(self):
        self.api(None, 'POST', self.prefix() + '/',
                 body={'user': {'username': 'user',
                                'password': THE_PASSWORD}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'}
                 )

        self.api(None, 'POST', self.prefix() + '/',
                 body={'user': {'username': 'admin',
                                'password': THE_PASSWORD,
                                'permission_flags': perm.ADMIN}},
                 expected_code=http.status.UNAUTHORIZED,
                 expected_result_subset={'id': 'NOT_ALLOWED_TO_REGISTER_ADMIN_USER'})

    def test_register_initial_admin_user(self):
        self.api(None, 'POST', self.prefix() + '/',
                 body={'user': {'username': 'admin',
                                'password': THE_PASSWORD,
                                'permission_flags': perm.ADMIN}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'}
                 )


class SetuUpTestUsersWithRegisteredAdmin(SetUpTestUserServiceBase):

    def setUp(self):
        # print("TestUsersWithRegisteredAdmin:setup()")
        super().setUp()
        # print("TestUsersWithRegisteredAdmin:setup() after super().setup()")

        self.api(None, 'POST', self.prefix() + '/',
                 body={'user': {'username': 'admin',
                                'password': THE_PASSWORD,
                                'permission_flags': perm.ADMIN}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'}
                 )

        self.id_admin = self.last_result['id']

        self.api(None, 'POST', self.prefix() + '/sessions/',
                 body={'username': 'admin',
                       'password': THE_PASSWORD},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id', 'token'}
                 )

        self.token_admin = self.last_result['token']
        # print("TestUsersWithRegisteredAdmin:/setup()")

class TestUsersWithRegisteredAdmin(SetuUpTestUsersWithRegisteredAdmin):

    def test_admin_fetch_list_of_users(self):

        self.api(self.token_admin, 'GET', self.prefix() + '/',
                 expected_code=http.status.OK,
                 expected_result_contain_keys={"summary", "users"},
                 expected_result_subset={"summary": {
                     "total_pages": 1,
                     "total_items": 1,
                     "page": 1,
                     "per_page": 10,
                     "next": None,
                     "previous": None
                 }}
                 )

        # self.show_last_result()

    def test_create_user_and_apply_admin_role(self):
        self.api(None, 'POST', self.prefix() + '/',
                 body={'user': {'username': 'new_admin',
                                'password': THE_PASSWORD,
                                'permission_flags': perm.ADMIN}},
                 expected_code=http.status.UNAUTHORIZED,
                 expected_result_subset={'id': 'NOT_ALLOWED_TO_REGISTER_ADMIN_USER'})

        self.api(None, 'POST', self.prefix() + '/',
                 body={'user': {'username': 'new_admin',
                                'password': THE_PASSWORD}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'})

        id_new_admin = self.last_result['id']

        # fetch all users
        self.api(self.token_admin, 'GET', self.prefix() + f'/', expected_code=http.status.OK,
                 expected_result_subset={
                     "summary": {
                         "total_pages": 1,
                         "total_items": 2,
                         "page": 1,
                         "per_page": 10,
                         "next": None,
                         "previous": None
                     }})

        # fetch all admins / expecting just one
        self.api(self.token_admin, 'GET', self.prefix() + f'/?permission_flags={perm.ADMIN}',
                 expected_code=http.status.OK,
                 expected_result_subset={
                     "summary": {
                         "total_pages": 1,
                         "total_items": 1,
                         "page": 1,
                         "per_page": 10,
                         "next": None,
                         "previous": None
                     }})

        # fetch all non admins / expecting just one
        self.api(self.token_admin, 'GET', self.prefix() + f'/?permission_flags={perm.USER}',
                 expected_code=http.status.OK,
                 expected_result_subset={
                     "summary": {
                         "total_pages": 1,
                         "total_items": 1,
                         "page": 1,
                         "per_page": 10,
                         "next": None,
                         "previous": None
                     }})

        # transform user into admin
        self.api(self.token_admin, 'PATCH', self.prefix() + f'/{id_new_admin}', body={'data': {
            'permission_flags': perm.USER | perm.ADMIN
        }}, expected_result=["permission_flags"])

        # fetch all admins / expecting 2 users
        self.api(self.token_admin, 'GET', self.prefix() + f'/?permission_flags={perm.ADMIN}',
                 expected_code=http.status.OK,
                 expected_result_subset={
                     "summary": {
                         "total_pages": 1,
                         "total_items": 2,
                         "page": 1,
                         "per_page": 10,
                         "next": None,
                         "previous": None
                     }})

        #! # fetch all non admins users
        # # still expecting 1 users, becaue new_admin is user and admin too.
        # self.api(self.token_admin, 'GET', self.prefix() + f'/?permission_flags={perm.USER}',
        #          expected_code=http.status.OK,
        #          expected_result_subset={
        #              "summary": {
        #                  "total_pages": 1,
        #                  "total_items": 1,
        #                  "page": 1,
        #                  "per_page": 10,
        #                  "next": None,
        #                  "previous": None
        #              }})


class TestUsersWithRegisteredAdminAndTwoNonAdminUsers(SetuUpTestUsersWithRegisteredAdmin):

    def setUp(self):
        super().setUp()
        print("OVDE NE SME NIKAD DA UDJE")

    # def setUp(self):
    #     super().setUp()
    #
    #     self.api(None, 'POST', self.prefix() + '/',
    #              body={'user': {'username': 'user',
    #                             'password': THE_PASSWORD}},
    #              expected_code=http.status.CREATED,
    #              expected_result_contain_keys={'id'})
    #
    #     self.id_user = self.last_result['id']
    #
    #     self.api(None, 'POST', self.prefix() + '/sessions/',
    #              body={'username': 'user', 'password': THE_PASSWORD},
    #              expected_code=http.status.CREATED,
    #              expected_result_contain_keys={'token', 'id'})
    #
    #     self.token_user = self.last_result['token']
    #
    #     self.api(None, 'POST', self.prefix() + '/',
    #              body={'user': {'username': 'user2',
    #                             'password': THE_PASSWORD}},
    #              expected_code=http.status.CREATED,
    #              expected_result_contain_keys={'id'})
    #
    #     self.id_user2 = self.last_result['id']
    #
    #     self.api(None, 'POST', self.prefix() + '/sessions/',
    #              body={'username': 'user2', 'password': THE_PASSWORD},
    #              expected_code=http.status.CREATED,
    #              expected_result_contain_keys={'token', 'id'})
    #
    #     self.token_user2 = self.last_result['token']

    # def test_user_change_preferences(self):
    #     # user changes his basic properties
    #     self.api(self.token_user, 'PATCH', self.prefix() + f'/{self.id_user}', body={
    #         'data': {'first_name': 'John',
    #                  'last_name': 'Doe',
    #                  'email': 'johndoe@example.com'}},
    #              expected_code=http.status.OK,
    #              expected_result=["email", "first_name", "last_name"])
    #
    #     # basic user (user) tries to change other user (user2) basic properties
    #     self.api(self.token_user, 'PATCH', self.prefix() + f'/{self.id_user2}', body={
    #         'data': {'first_name': 'John2',
    #                  'last_name': 'Doe2',
    #                  'email': 'johndoe2@example.com'}},
    #              expected_code=http.status.UNAUTHORIZED)
    #
    #     # admin user changes other user (user2) basic properties
    #     self.api(self.token_admin, 'PATCH', self.prefix() + f'/{self.id_user2}', body={
    #         'data': {'first_name': 'John2',
    #                  'last_name': 'Doe2',
    #                  'email': 'johndoe2@example.com'}},
    #              expected_code=http.status.OK,
    #              expected_result=["email", "first_name", "last_name"])

    # def test_user_change_own_password(self):
    #     # user tries to change password without providing old one
    #     self.api(self.token_user, 'PATCH', self.prefix() + f'/{self.id_user}', body={
    #         'data': {'password': THE_PASSWORD + '-updated'}},
    #              expected_code=http.status.UNAUTHORIZED,
    #              expected_result_subset={"id": "MISSING_PARAM_OLD_PASSWORD"})
    #
    #     # user tries to change his password by providing incorect old password
    #     self.api(self.token_user, 'PATCH', self.prefix() + f'/{self.id_user}', body={
    #         'data': {'old_password': THE_PASSWORD + '-incorect',
    #                  'password': THE_PASSWORD + '-updated'}},
    #              expected_code=http.status.UNAUTHORIZED)
    #
    #     # user successfully changes his password by providing old one
    #     self.api(self.token_user, 'PATCH', self.prefix() + f'/{self.id_user}', body={
    #         'data': {'old_password': THE_PASSWORD,
    #                  'password': THE_PASSWORD + '-updated'}},
    #              expected_code=http.status.OK)
    #
    #     # try to login user with old password
    #     self.api(None, 'POST', self.prefix() + '/sessions', body={'username': 'user',
    #                                                               'password': THE_PASSWORD},
    #              expected_code=http.status.UNAUTHORIZED)
    #
    #     # try to login user with new password
    #     self.api(None, 'POST', self.prefix() + '/sessions', body={'username': 'user',
    #                                                               'password': THE_PASSWORD + '-updated'},
    #              expected_code=http.status.CREATED,
    #              expected_result_contain_keys={'id', 'token'})
    #
    #     # admin changes password for target user without providing old password
    #     self.api(self.token_admin, 'PATCH', self.prefix() + f'/{self.id_user}', body={
    #         'data': {'password': 'a'}},
    #              expected_code=http.status.OK,
    #              expected_result=["password"])
    #
    #     # try to login user with new password
    #     self.api(None, 'POST', self.prefix() + '/sessions', body={'username': 'user',
    #                                                               'password': 'a'},
    #              expected_code=http.status.CREATED,
    #              expected_result_contain_keys={'id', 'token'})
    #
    #     # self.show_last_result()

if __name__ == '__main__':
    unittest.main()
