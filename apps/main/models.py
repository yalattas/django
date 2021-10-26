from django.db import models

# Create your models here.
class basicModelSample(models.Model):
    first_name = models.CharField(max_length=50,)
    middel_name = models.CharField(
        max_length=50, null=True, blank=True,)
    last_name = models.CharField(max_length=50,)
    email = models.EmailField()
    mobile_number = models.CharField( max_length=10)
    district = models.CharField(max_length=50)

    city_preferred_region = models.CharField(
        max_length=50
    )
    remark = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name + '(' + self.mobile_number + ')'