from django.contrib import admin
from django.urls import include, path

from polls.views import home

urlpatterns = [
    path('',home, name='home'),
    path('admin/', admin.site.urls),
    path('polls/',include('polls.urls',namespace='polls')),
    path('accounts/',include('accounts.urls',namespace='accounts'))
]
