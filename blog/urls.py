from django.urls import re_path,path
from . import views
# from django.contrib.auth import views
from django.urls import reverse_lazy


# from django.utils import timezone


urlpatterns = [
    re_path(r'^$', views.PublicListView.as_view(), name='public_list'),
    re_path(r'^list/$', views.PostListView.as_view(), name='post_list'),
    re_path(r'^about/$', views.AboutView.as_view(), name='about'),
    re_path(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    re_path(r'^post/new/$', views.CreatePostView.as_view(), name='post_new'),
    re_path(r'^post/(?P<pk>\d+)/edit/$', views.UpdatePostView.as_view(), name='post_edit'),
    re_path(r'^drafts/$', views.DraftPostView.as_view(), name='post_draft_list'),
    re_path(r'^post/(?P<pk>\d+)/remove/$', views.DeletePostView.as_view(), name='post_remove'),

    re_path(r'^post/(?P<pk>\d+)/register/$', views.RegisterToggle.as_view(), name='register'),

    re_path(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    re_path(r'^post/(?P<pk>\d+)/publishp/$', views.public_publish, name='public_publish'),

    re_path(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    re_path(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    re_path(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),

    # re_path(r'^read/$', views.Read.as_view(), name='read'),

    # path('pdf/',views.GeneratePdf.as_view()),

    path('email-form/',views.email_form, name='email_form'),
    path('department-form/',views.department_form, name='department_form'),
    path('catagory-form/',views.catagory_form, name='catagory_form'),




]

handler404 = views.handler404
error_500_view= views.error_500_view
notfound=views.notfound