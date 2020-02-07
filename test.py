from rest_framework import status
from rest_framework.test import APITestCase

ADDRESS_FOR_TEST = 'http://127.0.0.1:8000/add_comment'


class ApiOAuthTestCase(APITestCase):

    def setUp(self):
        self.my_message = {
            'uid': 1,
            'pid': 1,
            'text': 'some text',
        }

    def test_token(self):
        response = self.client.post(ADDRESS_FOR_TEST, self.my_message, content_type='application/json')
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)