from django.conf import settings


def google_analytics(request):
    if not settings.DEBUG and getattr(settings, 'GOOGLE_ANALYTICS', False):
        return {'GOOGLE_ANALYTICS': getattr(settings, 'GOOGLE_ANALYTICS', False)}
    return {}
