from seven_api.resources.HooksResource import HooksResource, HookEventType, HookRequestMethod
from tests.BaseTest import BaseTest


class TestHooks(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = HooksResource(self.client)

    def test_read(self) -> None:
        res = self.resource.subscribe({
            'event_type': HookEventType.SMS_INBOUND.value,
            'target_url': BaseTest.create_random_url(),
        })
        hook_id = res.id

        res = self.resource.read()

        self.assertTrue(res.success)

        for hook in res.hooks:
            self.assertGreater(len(hook.created), 0)
            self.assertIn(hook.event_type, HookEventType.values())
            self.assertRegex(hook.id, r'\d')
            self.assertIn(hook.request_method, HookRequestMethod.values())
            self.assertGreater(len(hook.target_url), 0)

        self.resource.unsubscribe(hook_id)

    def test_subscribe(self) -> None:
        params = {
            'event_filter': '491716992343',
            'event_type': HookEventType.SMS_INBOUND.value,
            'request_method': HookRequestMethod.GET.value,
            'target_url': BaseTest.create_random_url(),
        }
        res = self.resource.subscribe(params)
        self.assertGreater(res.id, 0)
        self.assertTrue(res.success)

        hooks = self.resource.read().hooks
        hook = next(x for x in hooks if x.id == str(res.id))
        self.assertEqual(params['event_filter'], hook.event_filter)
        self.assertEqual(params['event_type'], hook.event_type)
        self.assertEqual(params['request_method'], hook.request_method)
        self.assertEqual(params['target_url'], hook.target_url)

        self.resource.unsubscribe(res.id)

    def test_unsubscribe(self) -> None:
        hook_id = self.resource.subscribe({
            'event_type': HookEventType.SMS_INBOUND.value,
            'target_url': BaseTest.create_random_url(),
        }).id

        res = self.resource.unsubscribe(hook_id)
        self.assertTrue(res.success)
