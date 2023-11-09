from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.Dash.Index.as_view(), name="index"),
    path('login', views.Dash.Login.as_view(), name="login"),
    path('cadastro', views.Dash.Cadastro.as_view(), name="cadastro"),
    path('logout', views.Dash._LogOut.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)