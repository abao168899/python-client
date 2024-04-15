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

    def assert_group(self, group: dict) -> None:
        self.assertIsNotNone(group['created'])
        self.assertIsNotNone(group['id'])
        self.assertIsNotNone(group['members_count'])
        self.assertIsNotNone(group['name'])

    def test_groups_read(self) -> None:
        res_create = self.resource.create("Group Name")

        res = self.resource.list(GroupsListParams())
        self.assertIn('count', res['pagingMetadata'])
        self.assertIn('has_more', res['pagingMetadata'])
        self.assertIn('limit', res['pagingMetadata'])
        self.assertIn('offset', res['pagingMetadata'])
        self.assertIn('total', res['pagingMetadata'])

        for group in res['data']:
            self.assert_group(group)

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
        self.assert_group(group)

        self.resource.delete(create_res['id'])
