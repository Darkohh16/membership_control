from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    # auth
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # principal
    path("core/", include("core.urls")),
    # pagos
    path("pagos/", include("payments.urls")),
]
