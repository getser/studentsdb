# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


# Views for groups

def groups_list(request):
    groups = (
        {'id':1,
         'leader': {'id': 1, 'name': u'Гетьманчук'},
         'name': 'Мтм-223',},
        {'id':2,
         'leader': {'id': 2, 'name': u'Іванов'},
         'name': 'Мтм-221',},
        {'id':3,
         'leader': {'id': 3, 'name': u'Петров'},
         'name': 'Мтм-232',},
        {'id':4,
         'leader': {'id': 4, 'name': u'Дрозд'},
         'name': 'Мтм-234',},
        )

    return render(request, 'students/groups_list.html', {'groups':groups})
    # return HttpResponse('<h1>Groups Listing</h1>')


def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')


def groups_edit(request, gid):
    return HttpResponse('<h1>Group %s edit form</h1>' %gid)


def groups_delete(request, gid):
    return HttpResponse('<h1>Group %s delete form</h1>' %gid)
