from django.test import TestCase, Client
from django.urls import reverse
import time
from quotes.middleware import IP_REQUEST_LOGS, IP_REQUEST_LOGS_LOCK, RATE_LIMIT_PER_MINUTE, RATE_LIMIT_WINDOW_SECONDS

class RateLimitTests(TestCase):

    def setUp(self):
        # Clear the rate limit logs before each test
        with IP_REQUEST_LOGS_LOCK:
            IP_REQUEST_LOGS.clear()
        self.client = Client()
        self.quote_url = reverse('random_quote') # Make sure this matches your URL name

    def test_rate_limit_allows_initial_requests(self):
        for i in range(RATE_LIMIT_PER_MINUTE):
            response = self.client.get(self.quote_url)
            self.assertEqual(response.status_code, 200)

    def test_rate_limit_exceeds(self):
        # Make requests up to the limit
        for i in range(RATE_LIMIT_PER_MINUTE):
            response = self.client.get(self.quote_url)
            self.assertEqual(response.status_code, 200)

        # The next request should be rate-limited
        response = self.client.get(self.quote_url)
        self.assertEqual(response.status_code, 429)
        self.assertIn("Rate limit exceeded", response.json()['error'])

    def test_rate_limit_resets_after_window(self):
        # Make requests up to the limit
        for i in range(RATE_LIMIT_PER_MINUTE):
            response = self.client.get(self.quote_url)
            self.assertEqual(response.status_code, 200)

        # Wait for the rate limit window to pass
        time.sleep(RATE_LIMIT_WINDOW_SECONDS + 1)

        # Now, new requests should be allowed
        response = self.client.get(self.quote_url)
        self.assertEqual(response.status_code, 200)

    def test_multiple_ips_have_independent_rate_limits(self):
        # Simulate requests from two different IPs
        client1 = Client(REMOTE_ADDR='192.168.1.1')
        client2 = Client(REMOTE_ADDR='192.168.1.2')

        # Client 1 hits their limit
        for i in range(RATE_LIMIT_PER_MINUTE):
            response = client1.get(self.quote_url)
            self.assertEqual(response.status_code, 200)
        response = client1.get(self.quote_url)
        self.assertEqual(response.status_code, 429)

        # Client 2 should still be able to make requests
        response = client2.get(self.quote_url)
        self.assertEqual(response.status_code, 200)