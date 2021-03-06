"""vogon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, handler403
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework_nested import routers as nrouters
from annotations import views
from concepts import views as conceptViews


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'appellation', views.AppellationViewSet)
router.register(r'predicate', views.PredicateViewSet)
router.register(r'relation', views.RelationViewSet)
router.register(r'relationset', views.RelationSetViewSet)
router.register(r'text', views.TextViewSet)
router.register(r'repository', views.RepositoryViewSet)
router.register(r'temporalbounds', views.TemporalBoundsViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'concept', views.ConceptViewSet)
router.register(r'type', views.TypeViewSet)
router.register(r'textcollection', views.TextCollectionViewSet)

repository_router = nrouters.NestedSimpleRouter(router, r'repository', lookup='repository')
repository_router.register('collection', views.RemoteCollectionViewSet, base_name='repository')

remotecollection_router = nrouters.NestedSimpleRouter(repository_router, r'collection', lookup='collection')
remotecollection_router.register('resource', views.RemoteResourceViewSet, base_name='collection')


#Error Handlers
handler403 = 'annotations.views.custom_403_handler'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^accounts/profile/', views.dashboard, name='dashboard'),
    url(r'^accounts/projects/', views.user_projects, name='user_projects'),
    url(r'^accounts/settings/$', views.user_settings, name='settings'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/accounts/login/'}),
    url(r'^activity/$', views.recent_activity),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include(router.urls)),
    url(r'^rest/', include(repository_router.urls)),
    url(r'^rest/', include(remotecollection_router.urls)),
    url(r'^text/$', views.TextSearchView.as_view(), name='text_search'),
    url(r'^network/$', views.network, name="network"),
    url(r'^relationtemplate/add/$', views.add_relationtemplate, name="add_relationtemplate"),
    url(r'^relationtemplate/(?P<template_id>[0-9]+)/$', views.get_relationtemplate, name="get_relationtemplate"),
    url(r'^relationtemplate/(?P<template_id>[0-9]+)/create/$', views.create_from_relationtemplate, name="create_from_relationtemplate"),
    url(r'^relationtemplate[/]?$', views.list_relationtemplate, name='list_relationtemplate'),
    url(r'^network/data/$', views.network_data, name="network-data"),
    url(r'^network/text/(?P<text_id>[0-9]+)/$', views.network_for_text, name="network_for_text"),
    # url(r'^text/$', views.list_texts, name="list_texts"),
    url(r'^text/add/upload/$', views.upload_file, name="file_upload"),
    url(r'^text/(?P<textid>[0-9]+)/$', views.text, name="text"),
    url(r'^project/(?P<project_id>[0-9]+)/$', views.view_project, name='view_project'),
    url(r'^project/(?P<project_id>[0-9]+)/edit/$', views.edit_project, name='edit_project'),
    url(r'^project/create/$', views.create_project, name='create_project'),
    url(r'^project/$', views.list_projects, name='list_projects'),
    url(r'^collection/$', views.list_collections, name="collection_list"),
    url(r'^collection/(?P<collectionid>[0-9]+)/$', views.collection_texts, name="collection_texts"),
    url(r'^collection/text/add/$', views.add_text_to_collection, name="collection_addtext"),
    url(r'^users/$', views.list_user, name = 'users'),
    url(r'^users/(?P<userid>[0-9]+)/$', views.user_details, name="user_details"),
    url(r'^relations/(?P<source_concept_id>[0-9]+)/(?P<target_concept_id>[0-9]+)/$', views.relation_details, name="relation_details"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^$', views.home),
    url(r'^sign_s3$', views.sign_s3, name="sign_s3"),
    url(r'^concept/(?P<conceptid>[0-9]+)/$', views.concept_details, name='concept_details'),
    url(r'^concept/types$', conceptViews.list_concept_types),
    url(r'^concept/type/(?P<type_id>[0-9]+)/$', conceptViews.type, name="type"),
    url(r'^concept_autocomplete/', views.concept_autocomplete, name='concept_autocomplete'),
    url(r'^quadruples/appellation/(?P<appellation_id>[0-9]+).xml$', views.appellation_xml, name='appellation_xml'),
    url(r'^quadruples/relation/(?P<relation_id>[0-9]+).xml$', views.relation_xml, name='relation_xml'),
    url(r'^quadruples/relationset/(?P<relationset_id>[0-9]+).xml$', views.relationset_xml, name='relationset_xml'),
    url(r'^quadruples/text/(?P<text_id>[0-9]+)/(?P<user_id>[0-9]+).xml$', views.text_xml, name='text_xml'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
