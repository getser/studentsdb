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
        {'id':2,
         'first_name': u'Іван',
         'last_name': u'Іванов',
         'ticket': 7657,
         'image': 'img/podoba3.jpg'},
        {'id':3,
         'first_name': u'Василь',
         'last_name': u'Петров',
         'ticket': 9823,
         'image': 'img/piv.png'},
        {'id':4,
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
