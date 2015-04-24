import pytz
import json
import GeoIP as GeoIPC

from django.utils import timezone
from django.http import HttpResponse
from django.contrib.gis.geoip import GeoIP


class NonHtmlDebugToolbarMiddleware:
    """
    The Django Debug Toolbar usually only works for views that return HTML.
    This middleware wraps any non-HTML response in HTML if the request
    has a 'debug' query parameter (e.g. http://localhost/foo?debug)
    Special handling for json (pretty printing) and
    binary data (only show data length)
    """

    @staticmethod
    def process_response(request, response):
        if request.GET.get('debug') == '':
            if response['Content-Type'] == 'application/octet-stream':
                new_content = '<html><body>Binary Data, ' \
                    'Length: {}</body></html>'.format(len(response.content))
                response = HttpResponse(new_content)
            elif response['Content-Type'] != 'text/html':
                content = response.content
                try:
                    json_ = json.loads(content.decode('utf-8'))
                    content = json.dumps(json_, sort_keys=True, indent=2)
                except ValueError:
                    pass
                response = HttpResponse('<html><body><pre>{}'
                                        '</pre></body></html>'.format(content))

        return response


class TimezoneMiddleware:
    @staticmethod
    def process_response(request, response):
        # Uncomment for now
        # if request.COOKIES.get('timezone'):
        #    return response
        IP = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
        data = GeoIP().city(IP) or None
        _timezone = pytz.timezone(timezone.get_current_timezone_name())
        if data and data.get('country_code') and data.get('region'):
            _timezone = GeoIPC.time_zone_by_country_and_region(
                data.get('country_code'), data.get('region'))
            if _timezone:
                _timezone = pytz.timezone(_timezone)
            else:
                _timezone = pytz.timezone(timezone.get_current_timezone_name())
        response.set_cookie('timezone', _timezone.zone)
        return response
