# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


# Views for journals

def journal(request):
    return render(request, 'students/journal.html', {})


def journal_id(request, jid):
    return HttpResponse('<h1>Journal for student %s</h1>' %jid)
