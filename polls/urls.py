from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('create/', views.create_poll, name='create_poll'),
    path('my-polls/', views.my_polls, name='my_polls'),
    path('<str:poll_code>/', views.view_poll, name='view_poll'),
    path('<str:poll_code>/vote/', views.vote, name='vote'),
]
