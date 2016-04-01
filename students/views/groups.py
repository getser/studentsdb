# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from ..models import Group
from ..models.groups import Group
from ..models.students import Student

from django.core.urlresolvers import reverse

from django.views.generic import DeleteView
from django.db.models.deletion import ProtectedError



# Views for groups

def groups_list(request):

    groups = Group.objects.all()

    order_by = request.GET.get('order_by', '')

    if order_by in ('id', 'title', 'leader'):
        groups = groups.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()


    paginator = Paginator(groups, 4)
    page = request.GET.get('page', '')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    # hardcoded trial data set 
    # groups = (
    #     {'id':1,
    #      'leader': {'id': 1, 'second_name': u'Гетьманчук'},
    #      'title': 'Мтм-223',},
    #     {'id':2,
    #      'leader': {'id': 2, 'second_name': u'Іванов'},
    #      'title': 'Мтм-221',},
    #     {'id':3,
    #      'leader': {'id': 3, 'second_name': u'Петров'},
    #      'title': 'Мтм-232',},
    #     {'id':4,
    #      'leader': {'id': 4, 'second_name': u'Дрозд'},
    #      'title': 'Мтм-234',},
    #     )

    return render(request, 'students/groups_list.html', {'groups':groups})


def groups_add(request):
    if request.method == 'POST':
        if request.POST.get('add_button') is not None:
            errors = {}
            data = {'notes':request.POST.get('notes'),}

            title = request.POST.get('title')
            if not title:
                errors['title'] = u"Назва групи обов'язкова!"
            else:
                data['title'] = title

            leader = request.POST.get('leader')
            if leader:
                students = Student.objects.filter(pk=leader)
                if len(students) != 1:
                    errors['leader'] = u'Виберіть правильного студента.'
                else:
                    data['leader'] = students[0]
            if not errors:
                group = Group(**data)
                group.save()
                return HttpResponseRedirect(u'%s?status_message=Група %s успішно додана.' % (reverse('groups'), title))
            else:
                return render(request, 'students/groups_add.html',
                    {'students': Student.objects.all().order_by('last_name'),
                    'errors': errors})

        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect(u'%s?status_message=Додавання групи скасовано!' % reverse('groups'))
    else:
        return render(request, 'students/groups_add.html',
            {'students': Student.objects.all().order_by('last_name')})
    # return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Group %s edit form</h1>' %gid)


# def groups_delete(request, gid):
#     return HttpResponse('<h1>Group %s delete form</h1>' %gid)

class GroupDeleteView(DeleteView):
    """Class view for group delete"""

    model = Group
    template_name = 'students/groups_confirm_delete.html' # reassigning template name !!!

    def get_success_url(self):
        return u'%s?status_message=Gruop was succesfully deleted!' % reverse('groups')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """

        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            return HttpResponseRedirect(u'%s?status_message=Group %s deletion is impossible! It contains students. Please take away all students from this group.' % (reverse('groups'), str(kwargs['pk'])))

        return HttpResponseRedirect(success_url)

    # def post(self, request, *args, **kwargs):
    #     if request.POST.get('cancel_button'):
    #         return HttpResponseRedirect(u'%s?status_message=**да**ння групи скасовано!' % reverse('groups'))
    #     elif request.POST.get('delete_button'):
    #         return self.get_success_url()