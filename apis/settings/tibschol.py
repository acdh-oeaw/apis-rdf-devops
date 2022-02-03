
from .base import *
import re
import dj_database_url
import os


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "^mm-24*i-6iecm7c@z9l+7%^ns^4g^z!8=dgffg4ulggr-4=1%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# REDMINE_ID = "14590"
APIS_LIST_VIEWS_ALLOWED = False
APIS_DETAIL_VIEWS_ALLOWED = False
FEATURED_COLLECTION_NAME = "FEATURED"
# MAIN_TEXT_NAME = "ÖBL Haupttext"
BIRTH_REL_NAME = "geboren in"
DEATH_REL_NAME = "verstorben in"
APIS_LOCATED_IN_ATTR = ["located in"]
APIS_BASE_URI = "https://paas.acdh.oeaw.ac.at/"
# APIS_OEBL_BIO_COLLECTION = "ÖBL Biographie"

APIS_SKOSMOS = {
    "url": os.environ.get("APIS_SKOSMOS", "https://vocabs.acdh-dev.oeaw.ac.at"),
    "vocabs-name": os.environ.get("APIS_SKOSMOS_THESAURUS", "apisthesaurus"),
    "description": "Thesaurus of the APIS project. Used to type entities and relations.",
}

ALLOWED_HOSTS = re.sub(
    r"https?://",
    "",
    os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,paas.acdh-dev.oeaw.ac.at"),
).split(",")
# You need to allow '10.0.0.0/8' for service health checks.

ALLOWED_CIDR_NETS = ["10.0.0.0/8", "127.0.0.0/8"]

REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = (
    # "rest_framework.permissions.DjangoModelPermissions",
    "rest_framework.permissions.IsAuthenticated",
    # "rest_framework.permissions.DjangoObjectPermissions",
    # use IsAuthenticated for every logged in user to have global edit rights
)

# HAYSTACK_DEFAULT_OPERATOR = "OR"

SECRET_KEY = (
    "d3j@454545()(/)@zlck/6dsaf*#sdfsaf*#sadflj/6dsfk-11$)d6ixcvjsdfsdf&-u35#ayi"
)
DEBUG = True
DEV_VERSION = False

SPECTACULAR_SETTINGS["COMPONENT_SPLIT_REQUEST"] = True
SPECTACULAR_SETTINGS["COMPONENT_NO_READ_ONLY_REQUIRED"] = True

DATABASES = {}

DATABASES["default"] = dj_database_url.config(conn_max_age=600)

MAIN_TEXT_NAME = "ÖBL Haupttext"

LANGUAGE_CODE = "de"


#STATICFILES_DIRS = [BASE_DIR + "/member_images"]

# APIS_COMPONENTS = ['deep learning']

# APIS_BLAZEGRAPH = ('https://blazegraph.herkules.arz.oeaw.ac.at/metaphactory-play/sparql', 'metaphactory-play', 'KQCsD24treDY')
#INSTALLED_APPS += ["apis_ontology"]

APIS_RELATIONS_FILTER_EXCLUDE += ["annotation", "annotation_set_relation"]
