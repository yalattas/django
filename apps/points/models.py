from django.db import models

# Create your models here.
class Employee(models.Model):
    first_name = models.CharField(max_length=50,)
    last_name = models.CharField(max_length=50,)
    email = models.EmailField()
    mobile_number = models.CharField( max_length=10)
    remark = models.CharField(max_length=200)

    def get_all_employees(self):
        return self.Employee.objects.all()

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name + '(' + self.mobile_number + ')'