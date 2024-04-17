from seven_api.resources.GroupsResource import GroupsResource, GroupsListParams, Group
from tests.BaseTest import BaseTest


class TestGroups(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = GroupsResource(self.client)

    def test_groups_delete(self) -> None:
        res_create = self.resource.create("Group Name")
        group_id = res_create.id

        try:
            self.resource.delete(group_id)
        except ValueError:
            self.fail("delete() raised ValueError unexpectedly!")

    def __assert_group(self, group: Group) -> None:
        self.assertTrue(len(group.created) > 0)
        self.assertTrue(group.id > 0)
        self.assertTrue(group.members_count >= 0)
        self.assertTrue(len(group.name) > 0)

    def test_groups_list(self) -> None:
        res_create = self.resource.create("Group Name")

        params = GroupsListParams(limit=500)
        res = self.resource.list(params)
        self.assertTrue(res.pagingMetadata.count >= 0)
        self.assertEqual(params.limit, res.pagingMetadata.limit)
        self.assertTrue(res.pagingMetadata.offset >= 0)
        self.assertTrue(res.pagingMetadata.total >= 0)

        for group in res.data:
            self.__assert_group(group)

        self.resource.delete(res_create.id)

    def test_groups_create(self) -> None:
        name = "Group Name"
        res = self.resource.create(name)

        self.assertEqual(name, res.name)
        self.assertEqual(0, res.members_count)

        self.resource.delete(res.id)

    def test_groups_get(self) -> None:
        name = "Group Name"
        create_res = self.resource.create(name)

        group = self.resource.get(create_res.id)
        self.assertEqual(group.id, create_res.id)
        self.assertEqual(name, group.name)
        self.__assert_group(group)

        self.resource.delete(create_res.id)
