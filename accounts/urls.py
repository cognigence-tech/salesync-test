from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.connection_list, name='connection_list'),
    path('create/', views.create_connection, name='create-connection'),
]
