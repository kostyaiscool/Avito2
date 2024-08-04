from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

_swagger_urlpatterns = [
    path(
        "api/v1/schema/",
        extend_schema(exclude=True)(SpectacularAPIView).as_view(),
        name="schema",
    ),
    path(
        "docs/",
        extend_schema(exclude=True)(SpectacularSwaggerView).as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        extend_schema(exclude=True)(SpectacularRedocView).as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns = [
    *_swagger_urlpatterns,
    path("", lambda _request: redirect("docs/"), name="home"),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('shop/', include('coems.urls')),
]