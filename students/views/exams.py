# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.exams import Exam
from ..models.subjects import Subject
from ..models.teachers import Teacher
from ..models.groups import Group
from ..models.students import Student


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
    if request.method == 'POST':
        if request.POST.get('add_button'):
            data = {}
            errors = {}

            subject_id = request.POST.get('subject')
            if subject_id:
                subject = Subject.objects.filter(pk=subject_id)
                if len(subject) != 1:
                    errors['subject'] = "Choose correct subject!"
                else:
                    data['subject'] = subject[0]
            else:
                errors['subject'] = "Це поле обов'язкове."

            teacher_id = request.POST.get('teacher')
            if teacher_id:
                teacher = Teacher.objects.filter(pk=teacher_id)
                if len(teacher) != 1:
                    errors['teacher'] = "Choose correct teacher!"
                else:
                    data['teacher'] = teacher[0]
            else:
                errors['teacher'] = "Це поле обов'язкове."

            date_time = request.POST.get('date_and_time')
            if date_time:
                try:
                    datetime.strptime(date_time, '%Y-%m-%d %H:%M')
                except ValueError:
                    errors['date_and_time'] = "Enter correct date and time."
                else:
                    data['date_and_time'] = date_time

            else:
                errors['date_and_time'] = "Це поле обов'язкове."

            group_id = request.POST.get('student_group')
            if group_id:
                group = Group.objects.filter(pk=group_id)
                if len(group) != 1:
                    errors['student_group'] = "Choose correct group!"
                else:
                    data['student_group'] = group[0]
            else:
                errors['student_group'] = "Це поле обов'язкове."


            if errors:
                return render(request, 'students/exams_add.html',{
                    'errors': errors,
                    'data': data,
                    'teachers': Teacher.objects.all().order_by('last_name'),
                    'subjects': Subject.objects.all().order_by('title'),
                    'groups': Group.objects.all().order_by('title')
                    })
            else:

                exam = Exam(**data)
                exam.save()

                return HttpResponseRedirect(u'%s?status_message=Exam is successfuly added!' % reverse('exams'))
        else:
            return HttpResponseRedirect(u'%s?status_message=Додавання екзамена скасовано!' % reverse('exams'))
    else:
        return render(request, 'students/exams_add.html', {
            'teachers': Teacher.objects.all().order_by('last_name'),
            'subjects': Subject.objects.all().order_by('title'),
            'groups': Group.objects.all().order_by('title')
             })

    # return HttpResponse('<h1>Exam add form</h1>')


def exams_edit(request, eid):
    return HttpResponse('<h1>Exam %s edit form</h1>' %eid)


# def exams_delete(request, eid):
#     return HttpResponse('<h1>Exam %s delete form</h1>' %eid)

def exams_delete(request, pk):
    if request.method == 'GET':
        exam = Exam.objects.get(pk=pk)
        if exam:
            return render(request, 'students/exams_confirm_delete.html', {'object': exam})
        else:
            HttpResponseRedirect(u'%s?status_message=Виберіть коректний екзамен.' % reverse('exams'))
    elif request.method == 'POST':
        if request.POST.get('delete_button'):
            exam = Exam.objects.get(pk=pk)
            if exam:
                exam.delete()

                return HttpResponseRedirect(u'%s?status_message=Екзамен успішно відалено!' % reverse('exams'))

            else:
                HttpResponseRedirect(u'%s?status_message=Виберіть коректний екзамен.' % reverse('exams'))


        else:
            return HttpResponseRedirect(u'%s?status_message=Видалення екзамена скасовано!' % reverse('exams'))


    # return HttpResponse('<h1>Exam %s edit form</h1>' %pk)
