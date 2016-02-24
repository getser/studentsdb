# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from ..models import Group
from ..models.groups import Group


# Views for groups

def groups_list(request):

    groups = Group.objects.all()

    order_by = request.GET.get('order_by', '')

    if order_by in ('id', 'title', 'leader'):
        groups = groups.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()


    paginator = Paginator(groups, 3)
    page = request.GET.get('page', '')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

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
    return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Group %s edit form</h1>' %gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Group %s delete form</h1>' %gid)
