import unittest
from base import http, test
from unittest.mock import patch

from tests.test_base import token2user, SetUpTestContactServiceBase, mockJWT, id_session


async def mocked_ipc_call(request, service, method, endpoint, body=None):
    if (service, method, endpoint) == ('users', 'get', 'about'):
        return {"service": "users"}

    print('nema kombinacije rejzujem')
    raise NameError(f"MOCKED_IPC_CALL not implemented for {(service, method, endpoint)}")

@patch('base.token.token2user', token2user)
class Test(SetUpTestContactServiceBase):

    @patch('base.ipc.call', mocked_ipc_call)
    def test_ipc(self):
        self.api(None, 'GET', self.prefix() + '/test_ipc')
        self.show_last_result()

    def test(self):
        self.api(None, 'GET', self.prefix() + '/about', expected_code=http.status.OK,
                 expected_result={"service": "contacts"})

    def test_non_authorized_user_tries_to_fetch_list_of_contacts(self):
        self.api(None, 'GET', self.prefix() + '/', expected_code=http.status.UNAUTHORIZED)

    def test_authorized_user_fetch_list_of_contacts(self):
        self.api(mockJWT, 'GET', self.prefix() + '/', expected_code=http.status.OK)

    def test_user_add_contact(self):
        self.api(mockJWT, 'POST', self.prefix() + '/',
                 body={'contact': {'name': 'Nikola',
                                   'email': 'nikola.milisavljevic@digitalcube.rs'}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'})

        self.api(mockJWT, 'GET', self.prefix() + '/', expected_code=http.status.OK,
                 expected_result={
                     "summary": {
                         "total_pages": 1,
                         "total_items": 1,
                         "page": 1,
                         "per_page": 10,
                         "next": None,
                         "previous": None
                     },
                     "contacts": [
                         {
                             "name": "Nikola",
                             "email": "nikola.milisavljevic@digitalcube.rs"
                         }
                     ]
                 })

        self.api(mockJWT, 'POST', self.prefix() + '/',
                 body={'contact': {'name': 'Slobodan',
                                   'email': 'slobodan@digitalcube.rs'}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'})

        self.api(mockJWT, 'POST', self.prefix() + '/',
                 body={'contact': {'name': 'Igor',
                                   'email': 'igor@digitalcube.rs'}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'})

        self.api(mockJWT, 'GET', self.prefix() + '/', expected_code=http.status.OK,
                 expected_result_contain_keys={'summary', 'contacts'})

        self.assertTrue(self.last_result['summary']['total_items'] == 3)
        self.assertTrue(len(self.last_result['contacts']) == 3)

    def test_user_fetch_added_contact_by_id(self):
        self.api(mockJWT, 'POST', self.prefix() + '/',
                 body={'contact': {'name': 'Igor',
                                   'email': 'igor@digitalcube.rs'}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'})

        id_contact = self.last_result['id']

        self.api(mockJWT, 'GET', self.prefix() + f'/{id_contact}', expected_code=http.status.OK,
                 expected_result={
                     "name": "Igor",
                     "email": "igor@digitalcube.rs"
                 })

        # user tries to fetch non existing contact

        self.api(mockJWT, 'GET', self.prefix() + f'/{id_session}', expected_code=http.status.NOT_FOUND)

    def test_user_delete_contact(self):
        self.api(mockJWT, 'POST', self.prefix() + '/',
                 body={'contact': {'name': 'Igor',
                                   'email': 'igor@digitalcube.rs'}},
                 expected_code=http.status.CREATED,
                 expected_result_contain_keys={'id'})

        id_contact = self.last_result['id']

        self.api(mockJWT, 'GET', self.prefix() + '/', expected_code=http.status.OK)
        self.assertTrue(self.last_result['summary']['total_items'] == 1)
        self.assertTrue(len(self.last_result['contacts']) == 1)

        self.api(mockJWT, 'DELETE', self.prefix() + f'/{id_contact}', expected_code=http.status.NO_CONTENT)
        self.api(mockJWT, 'GET', self.prefix() + '/', expected_code=http.status.OK)

        self.assertTrue(self.last_result['summary']['total_items'] == 0)
        self.assertTrue(len(self.last_result['contacts']) == 0)


if __name__ == '__main__':
    unittest.main()
