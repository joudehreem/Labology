from django.db import models
import re
import bcrypt
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.


class UserManager(models.Manager):
    def basic_register(self, postData): # function for registration 
        errors = {}
        if len(postData['first_name']) < 2:# validated first name
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:# validated last name
            errors["last_name"] = "Last Name should be at least 2 characters"      
        #validated format of mail and unique email used
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):             
            errors['email'] = "Invalid email address!"
        if  Provider.objects.filter(email=postData['email']).exists():
            errors['email_used'] = "Email already in use!"
        # validated pass to be greater than 8 char and match with confirm pass 
        if len(postData['password']) < 4:
            errors["password"] = "Password should be at least 4 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords are not match "
        return errors
    
    def basic_login(self, postData):# function for login 
            errors = {}
            try:
                user = Provider.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors['email'] = "Email not found."
                return errors
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password."
            return errors

class Provider(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  role = models.CharField(max_length=50)
  clinic = models.CharField(max_length=50)
  email = models.EmailField(max_length=225)
  password = models.CharField(max_length=225)
  confirm_password = models.CharField(max_length=225)
  create_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()
  def __str__(self):
    return f'{self.first_name} {self.role}'
  
  
class Test(models.Model):
    IRON = 'IRON'
    VITAMIN_D = 'VITAMIN_D'
    TEST_TYPE_CHOICES = [
        (IRON, 'Iron'),
        (VITAMIN_D, 'Vitamin D'),
    ]
    NORMAL_RANGES = {
        IRON: '9-30.4',
        VITAMIN_D: '10-30',
    }
    type_of_test = models.CharField(
        max_length=20,
        choices=TEST_TYPE_CHOICES,
    )
    test_result = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type_of_test()} ({self.test_date})"

    # def is_within_normal_range(self):
    #     normal_range = self.NORMAL_RANGES.get(self.type_of_test, '0-0')
    #     if '-' in normal_range:
    #         try:
    #             min_value, max_value = normal_range.split('-')
    #             min_value, max_value = float(min_value), float(max_value)
    #             return min_value <= self.test_result <= max_value
    #         except ValueError:
    #             return False
    #     return False

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    mobile = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255,blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    description = models.TextField()
    episodes = models.ManyToManyField('Provider', related_name='patients')
    tests = models.ManyToManyField(Test, related_name='patients')
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# create user as a doctor or lab technicians 
def create_user(POST):
    password = POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return Provider.objects.create(
    first_name=POST['first_name'],
    last_name=POST['last_name'],
    role=POST['role'], 
    email=POST['email'], 
    password=hashed_password,  
    clinic=POST['clinic'],  
)

def get_user(session):
    return Provider.objects.get(id=session['user_id'])

def create_patient(POST):
    return Patient.objects.create(
    first_name=POST['first_name'],
    last_name=POST['last_name'],
    age=POST['age'],
    gender=POST['gender'],
    mobile=POST['mobile'],
    id_number=POST['id_number'],
    description=POST['description'],
    )

def patients():
    return Patient.objects.all()

def tests():
    return Test.objects.all()

def get_patient(patient_id):
    return Patient.objects.filter(id=patient_id).first()

def get_test(patient, test_id):
    return patient.tests.filter(id=test_id).first()



def crate_test(POST,id):
    patient = Patient.objects.filter(id=id).first()
    test = Test.objects.create(
        type_of_test=POST['type_of_test'],    
    )

    patient.tests.add(test)