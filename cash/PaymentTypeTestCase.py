import unittest
from django.test.client import Client

class PaymentTypeTestCase(TestCase):
    
    def test_index(self):
        response = self.client.get('/paymentType')
        self.failUnlessEqual(response.status_code, 200)
        