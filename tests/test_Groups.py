from seven_api.resources.GroupsResource import GroupsResource, GroupsListParams
from tests.BaseTest import BaseTest


class TestGroups(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = GroupsResource(self.client)

    def test_groups_delete(self) -> None:
        res_create = self.resource.create("Group Name")
        group_id = res_create['id']

        try:
            self.resource.delete(group_id)
        except ValueError:
            self.fail("delete() raised ValueError unexpectedly!")

    def __assert_group(self, group: dict) -> None:
        self.assertIsNotNone(group['created'])
        self.assertIsNotNone(group['id'])
        self.assertIsNotNone(group['members_count'])
        self.assertIsNotNone(group['name'])

    def test_groups_list(self) -> None:
        res_create = self.resource.create("Group Name")

        params = GroupsListParams()
        params.limit = 500
        res = self.resource.list(params)
        paging_metadata = res['pagingMetadata']
        self.assertIn('count', paging_metadata)
        self.assertIn('has_more', paging_metadata)
        self.assertIn('limit', paging_metadata)
        self.assertEqual(params.limit, paging_metadata['limit'])
        self.assertIn('offset', paging_metadata)
        self.assertIn('total', paging_metadata)

        for group in res['data']:
            self.__assert_group(group)

        self.resource.delete(res_create['id'])

    def test_groups_create(self) -> None:
        name = "Group Name"
        res = self.resource.create(name)

        self.assertEqual(name, res['name'])
        self.assertEqual(0, res['members_count'])

        self.resource.delete(res['id'])

    def test_groups_get(self) -> None:
        name = "Group Name"
        create_res = self.resource.create(name)

        group = self.resource.get(create_res['id'])
        self.assertEqual(group['id'], create_res['id'])
        self.assertEqual(name, group['name'])
        self.__assert_group(group)

        self.resource.delete(create_res['id'])
