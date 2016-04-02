# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from ..models import Group
from ..models.groups import Group
from ..models.students import Student

from django.core.urlresolvers import reverse

from django.views.generic import UpdateView, DeleteView
from django.db.models.deletion import ProtectedError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.forms import ModelForm



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


# def groups_edit(request, gid):
#     return HttpResponse('<h1>Group %s edit form</h1>' %gid)


class GroupUpdateForm(ModelForm):
    """Crispy forms class for student editing class view styling"""

    class Meta:
        model = Group
        fields = '__all__'
        # fields = ('first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'student_group', 'notes')
        # exclude = ()

    def __init__(self, *args, **kwargs):
        
        super(GroupUpdateForm, self).__init__(*args, **kwargs)


        self.helper = FormHelper(self)

        # set form tag attrbutes
        self.helper.form_action = reverse('groups_edit',
            kwargs={'pk':kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_reqired = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        # self.helper.layout[-1] = (FormActions( # - replaces last field in form with buttons
        self.helper.layout.append(FormActions(   # adds buttons after last field 
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
            ))


class GroupUpdateView(UpdateView):
    """View class for editing groups"""

    model = Group
    # fields = '__all__'

    template_name = 'students/groups_edit.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Групу успішно збережено!' % reverse('groups')


    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування групи відмінено!' % reverse('groups'))
        else:
            return super(GroupUpdateView, self).post(request, *args, **kwargs)


# def groups_delete(request, gid):
#     return HttpResponse('<h1>Group %s delete form</h1>' %gid)

class GroupDeleteView(DeleteView):
    """Class view for group delete"""

    model = Group
    template_name = 'students/groups_confirm_delete.html' # reassigning template name !!!

    def get_success_url(self):
        return u'%s?status_message=Група була успішно видалена!' % reverse('groups')

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
            return HttpResponseRedirect(u'%s?status_message=Ви не можете видалити групу %s! У ній є студенти. Будьласка, переведіть усих студентів із групи перед її видаленням!' % (reverse('groups'), str(kwargs['pk'])))

        return HttpResponseRedirect(success_url)

    # def post(self, request, *args, **kwargs):
    #     if request.POST.get('cancel_button'):
    #         return HttpResponseRedirect(u'%s?status_message=**да**ння групи скасовано!' % reverse('groups'))
    #     elif request.POST.get('delete_button'):
    #         return self.get_success_url()