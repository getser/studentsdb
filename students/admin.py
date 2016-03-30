# -*- coding: utf-8 -*-

from django.contrib import admin
# from .models import Student, Group
from .models.students import Student
from .models.groups import Group

from .models.exams import Exam
from .models.teachers import Teacher
from .models.subjects import Subject

from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError


class StudentFormAdmin(ModelForm):
    """docstring for StudentFormAdmin"""
    
    def  clean_student_group(self):
        """Check if student is leader in any group.
        if yes, then ensure it's the same as selected group."""
        # get group where current student is a leader
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(u'Студент є старостою іншої групи.', code='invalid')

        return self.cleaned_data['student_group']
        

class StudentAdmin(admin.ModelAdmin):
    """docstring for StudentAdmin"""
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket', 'notes']

    form = StudentFormAdmin

    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk':obj.id})


class GroupAdmin(admin.ModelAdmin):
    
    list_display = ['title', 'leader', 'notes']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['leader']
    list_per_page = 7
    search_fields = ['title', 'leader']

    # def view_on_site(self, obj):    
        # return reverse('')


# Register your models here.

admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)

admin.site.register(Exam)
admin.site.register(Teacher)
admin.site.register(Subject)