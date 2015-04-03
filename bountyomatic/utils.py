import pytz
import GeoIP as GeoIPC

from django.utils import timezone
from django.contrib.gis.geoip import GeoIP


def get_timezone_from_ip(ip):
    data = GeoIP().city(ip) or None
    _timezone = pytz.timezone(timezone.get_current_timezone_name())
    if data:
        _timezone = GeoIPC.time_zone_by_country_and_region(
            data.get('country_code'), data.get('region'))
        _timezone = pytz.timezone(_timezone)
    return _timezone.zone
