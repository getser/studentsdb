# -*- coding: utf-8 -*-
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic.base import TemplateView

from ..models.students import Student
from ..models.monthjournal import MonthJournal
from ..util import paginate


# Views for journals

# def journal(request):
#     return render(request, 'students/journal.html', {})


def journal_id(request, jid):
    return HttpResponse('<h1>Journal for student %s</h1>' %jid)


class JournalView(TemplateView):
    """docstring for JournalView"""
    template_name = 'students/journal.html'

    def post(self, request, *args, **kwargs):
        data = request.POST

        # prepare student, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        # get or create journal object for given student ad month
        journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]

        # set new  presence on journal for given student and save result
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()

        # return success result
        return JsonResponse({'status': 'success'})

    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if month is given in parameters,
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y-%m-%d').date()
        # if not - calculating current;
        else:
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # calculating current, next month and previous month
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)

        # for now they are static
        # context['prev_month'] = '2016-03-01'
        # context['next_month'] = '2016-05-01'
        # context['year'] = '2016'
        # context['cur_month'] = '2016-04-01'
        # context['month_verbose'] = u'April'

        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')

        # we'll use this variable in students pagiation
        context['cur_month'] = month.strftime('%Y-%m-%d')


        # here we are going to calculate month days list,
        # for now write them staically
        # context['month_header'] = [
        #     {'day':1, 'verbose': 'Mon'},
        #     {'day':2, 'verbose': 'Tw'},
        #     {'day':3, 'verbose': 'Wed'},
        #     {'day':4, 'verbose': 'Th'},
        #     {'day':5, 'verbose': 'Fr'}]

        # prepare the variable for template to generate
        # journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d,
            'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days+1)]

        # gettting all students sorted by last name
        queryset = Student.objects.order_by('last_name')

        # url to update student presence, for form post
        update_url = reverse('journal')  # this adress is for AJAX request

        # go over all students and collect data about presence
        # during selected month
        students = []
        for student in queryset:
            # try ot get journaal object by selected
            # month and current student
            try:
                journal = MonthJournal.objects.get(student=student, date=month)
            except Exception:
                journal = None

            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present_day%d' % day, False) or False,
                    'date': date(myear, mmonth, day).strftime('%Y-%m-%d'),
                    })

            # prepare metadata for current student
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
                })

        # applying pagination to students list
        context = paginate(students, 10, self.request, context, var_name='students')

        # return filled data dictionary
        return context            
