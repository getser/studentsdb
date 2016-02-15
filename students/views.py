# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


# Views for students

def students_list(request):
    students = (
        {'id':1,
         'first_name': u'Сергій',
         'last_name': u'Гетьманчук',
         'ticket': 2123,
         'image': 'img/me1.jpeg'},
        {'id':1,
         'first_name': u'Іван',
         'last_name': u'Іванов',
         'ticket': 7657,
         'image': 'img/podoba3.jpg'},
        {'id':1,
         'first_name': u'Василь',
         'last_name': u'Петров',
         'ticket': 9823,
         'image': 'img/piv.png'},
        {'id':1,
         'first_name': u'Сергій',
         'last_name': u'Дрозд',
         'ticket': 3405,
         'image': 'img/me4.jpeg'},
        )
                 
             # template = loader.get_template('students_list.html')
             # cont'ext = RequestContext(request, {})
    # return HttpResponse(template.render(context))
    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')


def students_edit(request, sid):
    return HttpResponse('<h1>Student %s edit form</h1>' %sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Student %s delete form</h1>' %sid)


# Views for groups

def groups_list(request):
    return HttpResponse('<h1>Groups Listing</h1>')


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Group %s edit form</h1>' %gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Group %s delete form</h1>' %gid)




# Views for journals

def journal(request):
    return HttpResponse('<h1>Journal</h1>')


def journal_id(request, jid):
    return HttpResponse('<h1>Journal for student %s</h1>' %jid)


