from django_mobile import flag_request_for_mobile

class MobileMiddleware(object):
    def process_request(self, request):
        request = flag_request_for_mobile(request)
        return None



