import time
from collections import deque
from threading import Lock
from django.http import JsonResponse

# In-memory storage for IP request logs:
# {
#     'ip_address': deque([timestamp1, timestamp2, ...])
# }
IP_REQUEST_LOGS = {}
IP_REQUEST_LOGS_LOCK = Lock() # For thread safety

RATE_LIMIT_PER_MINUTE = 5
RATE_LIMIT_WINDOW_SECONDS = 60

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply rate limiting to the /api/quote endpoint
        if not request.path == '/api/quote/':
            return self.get_response(request)

        ip_address = self.get_client_ip(request)
        current_time = time.time()

        with IP_REQUEST_LOGS_LOCK:
            if ip_address not in IP_REQUEST_LOGS:
                IP_REQUEST_LOGS[ip_address] = deque()

            # Remove timestamps older than the window
            while IP_REQUEST_LOGS[ip_address] and \
                  IP_REQUEST_LOGS[ip_address][0] < current_time - RATE_LIMIT_WINDOW_SECONDS:
                IP_REQUEST_LOGS[ip_address].popleft()

            if len(IP_REQUEST_LOGS[ip_address]) >= RATE_LIMIT_PER_MINUTE:
                # Calculate time to wait until next request is allowed
                time_elapsed_since_first_request = current_time - IP_REQUEST_LOGS[ip_address][0]
                time_to_wait = RATE_LIMIT_WINDOW_SECONDS - time_elapsed_since_first_request
                if time_to_wait < 0:
                    time_to_wait = 0 # Should not happen if deque is properly cleaned

                error_message = f"Rate limit exceeded. Try again in {int(time_to_wait) + 1} seconds."
                print(f"[{current_time}] Rate limit exceeded for IP: {ip_address} - Status: 429") # Logging
                return JsonResponse({"error": error_message}, status=429)
            else:
                IP_REQUEST_LOGS[ip_address].append(current_time)

        response = self.get_response(request)
        self.log_request(request, response, ip_address) # Logging
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def log_request(self, request, response, ip_address):
        current_time = time.time()
        print(f"[{current_time}] Client IP: {ip_address}, Request Path: {request.path}, Response Status: {response.status_code}")