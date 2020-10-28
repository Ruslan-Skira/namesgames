from django.contrib import admin
from .models import Contact, Student, Enrollment, Course
# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email")


admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Enrollment)
