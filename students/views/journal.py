# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from django.views.generic.base import TemplateView

from ..models.students import Student
from ..models.groups import Group


# Views for journals

# def journal(request):
#     return render(request, 'students/journal.html', {})


# def journal_id(request, jid):
#     return HttpResponse('<h1>Journal for student %s</h1>' %jid)


class JournalView(TemplateView):
    """docstring for JournalView"""
    template_name = 'students/journal.html'

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if month is given in parametr,
        # if not - calculating current;
        # now we are giving only current:

        today = datetime.today()
        month = date(today.year, today.month, 1)

        # calculating current year, next month and previous month
        # for now they are static
        context['prev_month'] = '2016-03-01'
        context['next_month'] = '2016-05-01'
        context['year'] = '2016'
        context['cur_month'] = '2016-04-01'
        context['month_verbose'] = u'April'

        # here we are going to calculate month days list,
        # for now write them staically
        context['month_header'] = [
            {'day':1, 'verbose': 'Mon'},
            {'day':2, 'verbose': 'Tw'},
            {'day':3, 'verbose': 'Wed'},
            {'day':4, 'verbose': 'Th'},
            {'day':5, 'verbose': 'Fr'}]

        # gettting all students sorted by last name
        queryset = Student.objects.order_by('last_name')

        # this adress is for AJAX request
        update_url = reverse('journal')

        # run thrue all students and collecting nesessary data
        students = []

        for student in queryset:
            # TODO: take a journal for student and choosen month
            # typing days for student
            days = []
            for day in range(1, 31):
                days.append({
                    'day': day,
                    'present': True,
                    'date': date(2016, 4, day).strftime('%Y-%m-%d'),
                    })

            # typing all rest of students data
            students.append({
                'full_name': u'%s %s' (students.last_name, students.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
                })

            # applying pagination to students list
            
