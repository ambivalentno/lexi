from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView

from lexi.apps.lection.views import (
    CourseListView, CourseDetailView, LessonDetailView, UnitDetailView
)


admin.autodiscover()

urlpatterns = patterns('',
    (r'^for-lecturers/', TemplateView.as_view(template_name="for-lecturers.html")),

    url(r'^courses/(?P<slug>[-_\w]+)/$',
        CourseDetailView.as_view(),
        name='course-detail'
    ),

    url(r'^courses/',
        CourseListView.as_view(),
        name='course-list'
    ),

    url(r'^lessons/(?P<slug>[-_\w]+)/$',
        LessonDetailView.as_view(),
        name='lesson-detail'
    ),

    url(r'^units/(?P<pk>\d+)/$',
        UnitDetailView.as_view(),
        name='unit-detail'
    ),

    # Apps and technical part
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', TemplateView.as_view(template_name="about.html")),

)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
