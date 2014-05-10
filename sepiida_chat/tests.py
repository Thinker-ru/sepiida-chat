from django.test import TestCase

from .models import Session


class SessionTestCase(TestCase):
    def test_e2e_basic(self):
        _ = self.client.get('/chat/widget.js')
        _ = self.client.post('/chat/send/', {'text': 'Test post. Please ignore.'})
