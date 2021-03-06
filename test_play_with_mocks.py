import json
from unittest import TestCase
from unittest.mock import Mock

import requests

UNKNOWN_METHOD_ERROR = {
    'ok': False,
    'error': 'unknown_method',
    'req_method': 'channels.list',
}
UNKNOWN_METHOD_ERROR_STRING = json.dumps(UNKNOWN_METHOD_ERROR)
UNMOCKED_ERROR = {'ok': False, 'error': 'not_authed'}


class TestClass(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.original_method_storage = {
            'original_session_get': requests.Session.get,
            'original_session_post': requests.Session.post,
            'original_get': requests.get,
            'original_post': requests.post,
        }

        def mocked_get(url, **kwargs):
            if any(api in url for api in ['im.', 'mpim.', 'channels.', 'groups.']):
                return Mock(content=UNKNOWN_METHOD_ERROR_STRING)
            return cls.original_method_storage['original_get'](url, **kwargs)

        def mocked_post(url, **kwargs):
            if any(api in url for api in ['im.', 'mpim.', 'channels.', 'groups.']):
                return Mock(content=UNKNOWN_METHOD_ERROR_STRING)
            return cls.original_method_storage['original_post'](url, **kwargs)

        def mocked_session_get(session_self, url, **kwargs):
            if any(api in url for api in ['im.', 'mpim.', 'channels.', 'groups.']):
                return Mock(content=UNKNOWN_METHOD_ERROR_STRING)
            return cls.original_method_storage['original_session_get'](session_self, url, **kwargs)

        def mocked_session_post(session_self, url, **kwargs):
            if any(api in url for api in ['im.', 'mpim.', 'channels.', 'groups.']):
                return Mock(content=UNKNOWN_METHOD_ERROR_STRING)
            return cls.original_method_storage['original_session_post'](session_self, url, **kwargs)

        requests.Session.get = mocked_session_get
        requests.Session.post = mocked_session_post
        requests.get = mocked_get
        requests.post = mocked_post

    @classmethod
    def tearDownClass(cls) -> None:
        requests.Session.get = cls.original_method_storage['original_session_get']
        requests.Session.post = cls.original_method_storage['original_session_post']
        requests.get = cls.original_method_storage['original_get']
        requests.post = cls.original_method_storage['original_post']

    def test_legit_api_get(self):
        response = requests.get('https://www.slack.com/api/conversations.list')
        self.assertEqual(json.loads(response.content), UNMOCKED_ERROR)

    def test_legit_api_post(self):
        response = requests.post('https://www.slack.com/api/conversations.create')
        self.assertEqual(json.loads(response.content), UNMOCKED_ERROR)

    def test_bad_api_get(self):
        response = requests.get('https://www.slack.com/api/channels.list')
        self.assertEqual(json.loads(response.content), UNKNOWN_METHOD_ERROR)

    def test_bad_api_post(self):
        response = requests.post('https://www.slack.com/api/channels.invite')
        self.assertEqual(json.loads(response.content), UNKNOWN_METHOD_ERROR)

    def test_legit_api_session_get(self):
        s = requests.Session()
        response = s.get('https://www.slack.com/api/conversations.list')
        self.assertEqual(json.loads(response.content), UNMOCKED_ERROR)

    def test_legit_api_session_post(self):
        s = requests.Session()
        response = s.post('https://www.slack.com/api/conversations.create')
        self.assertEqual(json.loads(response.content), UNMOCKED_ERROR)

    def test_bad_api_session_get(self):
        s = requests.Session()
        response = s.get('https://www.slack.com/api/channels.list')
        self.assertEqual(json.loads(response.content), UNKNOWN_METHOD_ERROR)

    def test_bad_api_session_post(self):
        s = requests.Session()
        response = s.post('https://www.slack.com/api/channels.invite')
        self.assertEqual(json.loads(response.content), UNKNOWN_METHOD_ERROR)

