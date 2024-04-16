from seven_api.resources.ContactsResource import ContactsResource, ContactsListParams
from tests.BaseTest import BaseTest


class TestContacts(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = ContactsResource(self.client)

    def test_contacts_delete(self) -> None:
        res_create = self.resource.create({})
        contact_id = res_create['id']

        try:
            self.resource.delete(contact_id)
        except ValueError:
            self.fail("delete() raised ValueError unexpectedly!")

    def __assert_contact(self, contact: dict) -> None:
        self.assertIsNotNone(contact['id'])

    def test_contacts_list(self) -> None:
        res_create = self.resource.create({})

        params = ContactsListParams()
        params.limit = 500
        res = self.resource.list(params)
        paging_metadata = res['pagingMetadata']
        self.assertIn('count', paging_metadata)
        self.assertIn('has_more', paging_metadata)
        self.assertEqual(params.limit, paging_metadata['limit'])
        self.assertIn('offset', paging_metadata)
        self.assertIn('total', paging_metadata)

        for contact in res['data']:
            self.__assert_contact(contact)

        self.resource.delete(res_create['id'])

    def test_contacts_create(self) -> None:
        avatar = 'https://avatars.githubusercontent.com/u/25985637'
        params = {
            'email': 'wh@tev.er',
            'firstname': 'Tom',
            'lastname': 'Tester',
            'mobile_number': '491716992343',
        }
        res = self.resource.create(params, avatar)

        self.assertEqual(avatar, res['avatar'])
        self.assertEqual(params['email'], res['properties']['email'])
        self.assertEqual(params['firstname'], res['properties']['firstname'])
        self.assertEqual(params['lastname'], res['properties']['lastname'])
        self.assertEqual(params['mobile_number'], res['properties']['mobile_number'])

        self.resource.delete(res['id'])

    def test_contacts_get(self) -> None:
        create_res = self.resource.create({})

        contact = self.resource.get(create_res['id'])
        self.assertEqual(contact['id'], str(create_res['id']))
        self.__assert_contact(contact)

        self.resource.delete(create_res['id'])
