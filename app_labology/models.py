from django.db import models

# Create your models here.

class Provider(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  role = models.CharField(max_length=50)
  clinic = models.CharField(max_length=50)
  email = models.EmailField(max_length=225)
  password = models.CharField(max_length=225)
  create_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f'{self.first_name} {self.role}'

class Test(models.Model):
  test_date = models.DateField()
  type_of_test = models.CharField(max_length=255)
  test_result = models.CharField(max_length=255)
  create_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f" {self.type_of_test} {self.test_date}"

class Patient(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  age = models.IntegerField()
  gender = models.CharField(max_length=255)
  episodes= models.ManyToManyField(Provider, related_name='patients')
  result_test = models.ForeignKey(Test, on_delete=models.CASCADE)
  create_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f'{self.first_name} {self.last_name}'