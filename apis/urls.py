from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from django.urls import path

from apis_core.apis_entities.api_views import GetEntityGeneric

if "theme" in settings.INSTALLED_APPS:
    urlpatterns = [
        path("apis/", include("apis_core.urls", namespace="apis")),
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            "entity/<int:pk>/", GetEntityGeneric.as_view(), name="GetEntityGenericRoot"
        ),
        path("admin/", admin.site.urls),
        path("info/", include("infos.urls", namespace="info")),
        path("webpage/", include("webpage.urls", namespace="webpage")),
        path("/", include("theme.urls", namespace="theme")),
    ]
if "paas_theme" in settings.INSTALLED_APPS:
    urlpatterns = [
        path("apis/", include("apis_core.urls", namespace="apis")),
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            "entity/<int:pk>/", GetEntityGeneric.as_view(), name="GetEntityGenericRoot"
        ),
        path("admin/", admin.site.urls),
        path("info/", include("infos.urls", namespace="info")),
        path("webpage/", include("webpage.urls", namespace="webpage")),
        path("/", include("paas_theme.urls", namespace="theme")),
    ]
else:
    urlpatterns = [
        path("apis/", include("apis_core.urls", namespace="apis")),
        path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
        path(
            "entity/<int:pk>/", GetEntityGeneric.as_view(), name="GetEntityGenericRoot"
        ),
        path("admin/", admin.site.urls),
        path("info/", include("infos.urls", namespace="info")),
        path("", include("webpage.urls", namespace="webpage")),
    ]


if "viecpro_vis" in settings.INSTALLED_APPS:
    urlpatterns.insert(
        0, path("visualisations/", include("viecpro_vis.urls", namespace="viecpro_vis"))
    )

if "transkribus" in settings.INSTALLED_APPS:
    urlpatterns = urlpatterns + [
        path("transkribus/", include("transkribus.urls")),
    ]
"""
if "apis_bibsonomy" in settings.INSTALLED_APPS:
    urlpatterns.append(
        path("bibsonomy/", include("apis_bibsonomy.urls", namespace="bibsonomy"))
    )
"""
if "oebl_irs_workflow" in settings.INSTALLED_APPS:
    urlpatterns.append(
        path(
            "workflow/",
            include("oebl_irs_workflow.urls", namespace="oebl_irs_workflow"),
        )
    )
handler404 = "webpage.views.handler404"
