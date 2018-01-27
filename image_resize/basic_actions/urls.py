from django.conf.urls import url

from basic_actions import views

urlpatterns = [
    url(r'^(?P<image_hash>\w{32})/$', views.image_page, name='show_image'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^$', views.main_page, name='main_page'),
]
