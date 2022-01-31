from django.conf import settings
from . utils import PROJECT_METADATA
from . utils import PROJECT_TITLE_IMG, PROJECT_LOGO, PROJECT_CSS, SHARED_URL


def apis_app_name(request):
    return {'PROJECT_NAME': settings.PROJECT_NAME}


def shared_url(request):
    return {'SHARED_URL': SHARED_URL}


def title_img(request):
    return {'PROJECT_TITLE_IMG': PROJECT_TITLE_IMG}


def logo_img(request):
    return {'PROJECT_LOGO': PROJECT_LOGO}


def custom_css(request):
    return {'PROJECT_CSS': PROJECT_CSS}


def installed_apps(request):
    return {'APPS': settings.INSTALLED_APPS}


def is_dev_version(request):
    try:
        return {'DEV_VERSION': settings.DEV_VERSION}
    except AttributeError:
        return {}


def get_db_name(request):
    try:
        db_name = settings.DATABASES['default']['NAME']
        return {'DB_NAME': db_name}
    except Exception as e:
        return {}
