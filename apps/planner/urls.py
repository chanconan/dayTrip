from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^plan$', views.plan),
    url(r'^newplan$', views.newplan),
    url(r'^activity/(?P<plan_id>\d+)$', views.activity),
    url(r'^activity/(?P<plan_id>\d+)/add$', views.addActivity),
    url(r'^activity/(?P<plan_id>\d+)/show$', views.showPlan),
    url(r'^activity/(?P<plan_id>\d+)/delete/(?P<activity_id>\d+)$', views.deleteActivity),
    url(r'^logout$', views.logout)

]
