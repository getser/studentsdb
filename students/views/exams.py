# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.exams import Exam


# Views for exams

def exams_list(request):

    exams = Exam.objects.all()

    order_by = request.GET.get('order_by', '')

    if order_by in ('id', 'subject', 'teacher', 'student_group'):
        exams = exams.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()


    paginator = Paginator(exams, 3)
    page = request.GET.get('page', '')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        exams = paginator.page(1)
    except EmptyPage:
        exams = paginator.page(paginator.num_pages)

    # exams = (
    #     {'id':1,
    #      'teacher': {'id': 1, 'second_name': u'Гетьманчук'},
    #      'group': 'Мтм-223',
    #      'subject': 'Math'},
    #     {'id':2,
    #      'teacher': {'id': 2, 'second_name': u'Іванов'},
    #      'group': 'Мтм-221',
    #      'subject': 'Phys'},
    #     {'id':3,
    #      'teacher': {'id': 3, 'second_name': u'Петров'},
    #      'group': 'Мтм-232',
    #      'subject': 'Biology'},
    #     {'id':4,
    #      'teacher': {'id': 4, 'second_name': u'Дрозд'},
    #      'group': 'Мтм-234',
    #      'subject': 'Chemistry'},
    #     )

    return render(request, 'students/exams_list.html', {'exams': exams})


def exams_add(request):
    return HttpResponse('<h1>Exam add form</h1>')


def exams_edit(request, eid):
    return HttpResponse('<h1>Exam %s edit form</h1>' %eid)


def exams_delete(request, eid):
    return HttpResponse('<h1>Exam %s delete form</h1>' %eid)
