# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
# from ..models import Student
from ..models.students import Student
from ..models.groups import Group

from datetime import datetime


from django.template.defaultfilters import filesizeformat
from django.conf import settings
from PIL import Image


from django.forms import ModelForm

from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


# from django.core.context_processors import csrf

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Views for students

def students_list(request):

    students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('id','last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)

        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paging students withuot Paginator
    items_per_page = 5       # !! can't be less than 1 !!
    num_items = len(students)
    num_pages = num_items / items_per_page

    if num_items % items_per_page != 0:
        num_pages += 1

    page_str = request.GET.get('page','')

    try:
        page = int(page_str)
    except:
        page = 1

    if page < 1:
        page = 1
    elif page > num_pages:
        page = num_pages


    start = (page - 1) * items_per_page   # for 'standart' pagination

    # start = 0                          # for 'load more' pagination

    finish = page * items_per_page

    if finish > num_items:
        finish = num_items

    students = students[start:finish]

    paging = {
        'has_more_pages': len(students) < len(Student.objects.all()),
        'num_pages': num_pages,
        'curr_page': page,
        'next_page': page+1,
        'all_pages': range(1, num_pages + 1),
        }

    # paging students with Paginator
    # paginator = Paginator(students, 4)
    # page = request.GET.get('page')

    # try:
    #     students = paginator.page(page)
    # except PageNotAnInteger:
    #     students = paginator.page(1)
    # except EmptyPage:
    #     students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html',
        {
        'students': students,
        'paging': paging,
        })


def students_add(request):
    if request.method == 'POST':
    # if form method is POST:
        if request.POST.get('add_button') is not None:
        # if submit button is pressed:
            errors = {}
            # cheking data for correctness and collecting mistakes
            data = {'middle_name': request.POST.get('middle_name'),
                     'notes': request.POST.get('notes')}

            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Білет є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                # if photo._size > 1024:
                if photo._size > settings.MAX_UPLOAD_SIZE:
                    errors['photo'] = u"Файл занадто великий"
                else:
                    try:
                        Image.open(photo)                   
                        data['photo'] = photo
                    except:
                        errors['photo'] = u"Undefined image type"

            # if all data is not correct
                # return form template with found mistakes
            if not errors:
            # if all data is correct:
                # create and save student to database
                student = Student(
                    **data
                    # first_name=request.POST['first_name'],
                    # last_name=request.POST['last_name'],
                    # middle_name=request.POST['middle_name'],
                    # birthday=request.POST['birthday'],
                    # ticket=request.POST['ticket'],
                    # student_group=Group.objects.get(pk=request.POST['student_group']),
                    # photo=request.FILES['photo'],
                    # notes=request.POST['notes'],
                    )
                student.save()
                # return to students list
                return HttpResponseRedirect(u'%s?status_message=Студента %s %s успішно додано!' % (reverse('home'),
                    first_name, last_name))
            else:
                return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),
                    'errors': errors})
        elif request.POST.get('cancel_button') is not None:     
        # if cancel button pressed:
            # return to students list
            return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
    else:        
    # if form method is not POST:        
        # return form in start state
        return render(request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title')})

    # return HttpResponse('<h1>Student add form</h1>')
    # return render(request, 'students/students_add.html',
    #     {'groups': Group.objects.all().order_by('title')})


# def students_edit(request, sid):
#     return HttpResponse('<h1>Student %s edit form</h1>' %sid)


# def students_delete(request, sid):
#     return HttpResponse('<h1>Student %s delete form</h1>' %sid)


class StudentList(ListView):
    model = Student
    context_object_name = 'students'
    template = 'students/student_class_based_view_template'

    def get_context_data(self, **kwargs):
        """This method adds exttra variables to template"""
        # get original context data from parent class
        context = super(StudentList, self).get_context_data(**kwargs)

        # tell template not to show logo on a page
        context['show_logo'] = False

        # return context mapping

        return context

    def get_queryset(self):
        """Order students by last_name."""
        # get original queryset()
        qs = super(StudentList, self).get_queryset()

        # order by last name
        return qs.order_by('last_name')



class StudentUpdateForm(ModelForm):
    """Crispy forms class for student editing class view styling"""

    class Meta:
        model = Student
        fields = '__all__'
        # fields = ('first_name', 'last_name', 'middle_name', 'birthday', 'photo', 'ticket', 'student_group', 'notes')
        # exclude = ()

    def __init__(self, *args, **kwargs):
        
        super(StudentUpdateForm, self).__init__(*args, **kwargs)


        self.helper = FormHelper(self)

        # set form tag attrbutes
        self.helper.form_action = reverse('students_edit',
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


class StudentUpdateView(UpdateView):
    """View class for editing students"""

    model = Student
    # fields = '__all__'

    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        return u'%s?status_message=Студента успішно збережено!' % reverse('home')


    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Редагування студента відмінено!' % reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)


class StudentDeleteView(DeleteView):
    """View class for deleting students"""
    model = Student
 
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Студента успішно видалено!' % reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(u'%s?status_message=Видалення студента відмінено!' % reverse('home'))
