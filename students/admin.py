from django.contrib import admin
# from .models import Student, Group
from .models.students import Student
from .models.groups import Group

from .models.exams import Exam
from .models.teachers import Teacher
from .models.subjects import Subject

# Register your models here.

admin.site.register(Student)
admin.site.register(Group)

admin.site.register(Exam)
admin.site.register(Teacher)
admin.site.register(Subject)