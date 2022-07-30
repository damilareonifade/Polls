from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('list/',views.poll_list, name='list'),
    path('details/<slug:id>',views.poll_details,name='polls_details'),
]