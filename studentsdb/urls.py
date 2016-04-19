"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
# from django.conf.urls import url
from django.contrib import admin

from students.views import students, groups, journal, exams, contact_admin

from .settings import MEDIA_ROOT, DEBUG
# from django.contrib.staticfiles import views
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import patterns, url
from students.views.students import StudentList, StudentAddView, StudentUpdateView, StudentDeleteView
from students.views.groups import GroupAddView, GroupUpdateView, GroupDeleteView
from students.views.journal import JournalView




urlpatterns = [

    # students urls
    url(r'^$', students.students_list, name='home'),
    # url(r'^students/add/$', students.students_add, name='students_add'),
    url(r'^students/add/$', StudentAddView.as_view(), name='students_add'),
    # url(r'^students/(?P<sid>\d+)/edit/$', students.students_edit, name='students_edit'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    # url(r'^students/(?P<sid>\d+)/delete/$', students.students_delete, name='students_delete'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(), name='students_delete'),
    url(r'^student_list/$', StudentList.as_view()),



    # groups urls
    url(r'^groups/$', groups.groups_list, name='groups'),
    # url(r'^groups/add/$', groups.groups_add, name='groups_add'),
    url(r'^groups/add/$', GroupAddView.as_view(), name='groups_add'),
    # url(r'^groups/(?P<gid>\d+)/edit/$', groups.groups_edit, name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/edit/$', GroupUpdateView.as_view(), name='groups_edit'),
    # url(r'^groups/(?P<gid>\d+)/delete/$', groups.groups_delete, name='groups_delete'),
    url(r'^groups/(?P<pk>\d+)/delete/$', GroupDeleteView.as_view(), name='groups_delete'),



    # exams urls
    url(r'^exams/$', exams.exams_list, name='exams'),
    url(r'^exams/add/$', exams.exams_add, name='exams_add'),
    url(r'^exams/(?P<eid>\d+)/edit/$', exams.exams_edit, name='exams_edit'),
    # url(r'^exams/(?P<eid>\d+)/delete/$', exams.exams_delete, name='exams_delete'),
    url(r'^exams/(?P<pk>\d+)/delete/$', exams.exams_delete, name='exams_delete'),


    # journal urls
    # url(r'^journal/$', journal.journal, name='journal'),
    # url(r'^journal/(?P<jid>\d+)/$', journal.journal_id, name='journal_id'),
    # url(r'^journal/$', JournalView.as_view(), name='journal'),
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),


    url(r'^admin/', admin.site.urls),
    # url(r'^contact-admin/$', contact_admin.contact_admin, name='contact_admin'),
    url(r'^contact-admin/$', contact_admin.ContactView.as_view(), name='contact_admin'),
    # url(r'^contact/', include('contact_form.urls')),
    # url(r'^contact/$', include('contact_form.urls'), name='contact'),


    
]

if DEBUG:
    #serve files from media folder
     #    urlpatterns += [url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
     # {'document_root': MEDIA_ROOT}
     # ),]
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
