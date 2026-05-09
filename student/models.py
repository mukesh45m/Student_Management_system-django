from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField(unique=True)
    year = models.IntegerField()

    def __str__(self):
        return self.name
    
class Marks(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    def __str__(self):
        return self.subject


