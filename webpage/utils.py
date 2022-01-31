import requests

from django.conf import settings

PROJECT_STATIC_URL = "{}{}".format(settings.PROJECT_SHARED, settings.PROJECT_NAME)
PROJECT_MD_URL = "{}/metadata.json".format(PROJECT_STATIC_URL)

try:
    PROJECT_TITLE_IMG = settings.CUSTOM_TITLE_IMG
except AttributeError:
    PROJECT_TITLE_IMG = "{}/project-title-img.jpg".format(PROJECT_STATIC_URL)

try:
    PROJECT_LOGO = settings.CUSTOM_LOGO_IMG
except AttributeError:
    PROJECT_LOGO = "{}/project-logo.jpg".format(PROJECT_STATIC_URL)

try:
    PROJECT_CSS = settings.CUSTOM_CSS
except AttributeError:
    PROJECT_CSS = "{}/style.css".format(PROJECT_STATIC_URL)


def get_project_md():
    try:
        r = requests.get(PROJECT_MD_URL)
    except Exception as e:
        print(e)
        return settings.PROJECT_DEFAULT_MD
    if r.status_code == 200:
        return r.json()
    else:
        return settings.PROJECT_DEFAULT_MD


PROJECT_METADATA = get_project_md()

SHARED_URL = settings.SHARED_URL
