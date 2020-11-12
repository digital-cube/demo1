import base
from base import http
from base import paginate

if base.config.conf['apptype'] == 'monolith':
    base.route.set('prefix', base.config.conf['services']['contacts']['prefix'])
else:
    base.route.set('prefix', base.config.conf['prefix'])


import orm.models as models


@base.route('/about')
class AboutContactsServiceHandler(base.Base):

    @base.api()
    async def get(self):
        return {'service': 'contacts'}


async def ttt():
    return 'ttt'


@base.route('/test_ipc')
class TestHandler(base.Base):

    @base.api()
    async def get(self):
        return await base.ipc.call(self.request, 'users', 'get', 'about')


@base.route('')
class ContactsRouteHandler(base.Base):

    @base.auth()
    @base.api()
    async def get(self, page: int = 1, per_page: int = 10, search: str = None):

        filters = [models.Contact.id_owner == self.id_user]

        query, summary = paginate(
            self.orm_session.query(models.Contact).filter(*filters),
            base_uri=base.route.get('prefix') + '/',
            page=page, per_page=per_page)

        return {'summary': summary,
                'contacts': [c.serialize(['name', 'email']) for c in query.all()]}

    @base.auth()
    @base.api()
    async def post(self, contact: models.Contact):

        if not contact:
            raise base.http.HttpInvalidParam(id_message='INVALID_DATA_INPUT_FORMAT',
                                             message='Invalid data input format')

        contact.id_owner = self.id_user

        self.orm_session.add(contact)
        try:
            self.orm_session.commit()
        except:
            self.orm_session.rollback()
            raise base.http.HttpInternalServerError(id_message='DATABASE_ERROR',
                                                    message='Error writting object to database')

        return {'id': contact.id}, http.status.CREATED


@base.route('/:id_contact')
class SingleContactRouteHandler(base.Base):

    def can_use(self, contact):
        if not contact:
            raise http.HttpErrorNotFound

        if contact.id_owner != self.id_user:
            raise http.HttpErrorUnauthorized

    @base.auth()
    @base.api()
    async def get(self, contact: models.Contact.id, fields: str = 'name,email'):
        self.can_use(contact)
        return contact.serialize(fields.split(','))

    @base.auth()
    @base.api()
    async def delete(self, contact: models.Contact.id):
        self.can_use(contact)
        self.orm_session.delete(contact)
        try:
            self.orm_session.commit()
        except Exception as e:
            self.orm_session.rollback()
            raise http.HttpInternalServerError

        return None
