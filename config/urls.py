# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # 💥 Garanta que esta linha está presente e correta:
    # A string 'frota.urls' faz o Django procurar o arquivo urls.py DENTRO da aplicação 'frota'.
    path("api/", include("frota.urls")),
]
