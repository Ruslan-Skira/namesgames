from django.db import models

# Create your models here.
from django.db import models



class Contact(models.Model):
    """ Email subscription"""
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return f'name: {self.name} \n email: {self.email}'


class Student(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=30)
    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField()
    final_grade = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_combinations')
        ]

    # class Meta:
    #     unique_together = [['student', 'course']]
