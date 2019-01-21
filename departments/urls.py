from django.conf.urls import url

from . import views

app_name = 'departments'

urlpatterns = [
    url(r'create_message/$', views.CreateMessage.as_view(), name='create_message'),
    url(r'success/$', views.SuccessMessage.as_view(), name='success_message'),
    url(r'csv/$', views.some_view, name='csv'),
]