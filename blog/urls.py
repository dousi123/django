from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blog$', views.index, name='index'),
    url(r'^blog/(?P<article_id>[0-9]+)/$', views.showArticle, name='showArticle'),
    url(r'^blog/(?P<article_id>[0-9]+)/del$', views.delArticle, name='delArticle'),
    url(r'^blog/(?P<edu_id>[0-9]+)/eduDel$', views.delEdu, name='delEdu'),
    url(r'^blog/addArticle/', views.addArticle, name='addArticle'),
    # url(r'^login/', views.login, name='login'),
    # url(r'^register/', views.register, name='register'),

    # url(r'^showArticle/', views.showArticle, name='showArticle'),
    # url(r'^addComment/', views.addComment, name='addComment'),
]