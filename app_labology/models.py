from django.db import models
import re
import bcrypt
from django.core.exceptions import ObjectDoesNotExist

# validation to patient register

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
                # Validate user provider and uniqe email
                user = Provider.objects.get(email=postData['email'])
            except ObjectDoesNotExist:
                errors['email'] = "Email not found."
                return errors
            # Validate to same pass for user
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = "Invalid password."
            return errors
    def basic_patient(self, postData): # function for patient
        errors = {}
        # Validate First name
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        # Validate last name
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        # Validate Mobile
        if len(postData['mobile']) < 10:
            errors["mobile"] = "Mobile should be at least 10 characters"
        # Validate ID number
        if len(postData['id_number']) < 10:
            errors["id_number"] = "ID Number should be at least 10 characters"
        if Patient.objects.filter(id_number=postData['id_number']).exists():
            errors['id_number'] = "ID Number already in use!"
        # Validate description
        if len(postData['description']) < 20:
            errors["description"] = "Description should be at least 20 characters"
        # Validate gender
        if 'gender' not in postData or postData['gender'] not in ['male', 'female']:
            errors["gender"] = "Gender must be selected"



        return errors


        
class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Provider(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  
    clinic = models.CharField(max_length=50)
    email = models.EmailField(max_length=225)
    password = models.CharField(max_length=225)
    confirm_password = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role.name})'
    
    
class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    mobile = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    description = models.TextField()
    episodes = models.ManyToManyField(Provider, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Test(models.Model):
    type_of_test = models.CharField(max_length=225)
    normal_range = models.CharField(max_length=50)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.type_of_test}"


class PatientTest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    test_result = models.FloatField(blank=True, default=0)

# create user as a doctor or lab technicians 
def create_user(POST):
    password = POST['password']
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    role_id = POST.get('role')    
    role = Role.objects.get(id=role_id)
    return Provider.objects.create(
        first_name=POST['first_name'],
        last_name=POST['last_name'],
        role=role,
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
    
def add_provider(session,id):
    provider= get_user(session)
    patient = Patient.objects.get(id=id)
    patient.episodes.add(provider)
    

def patients():
    return Patient.objects.all()

def tests():
    return Test.objects.all()

def get_patient(patient_id):
    return Patient.objects.filter(id=patient_id).first()

def create_test(POST,id):
    patient = Patient.objects.get(id=id)
    test_id=POST['type_of_test']
    test = Test.objects.get(id=test_id)
    PatientTest.objects.create(patient=patient, test=test)
    
def update_test(POST,id):
    patient_test = PatientTest.objects.get(id=id)
    patient_test.test_result = POST['test_result']
    patient_test.save()

def patient_update(POST,id):
    patient = Patient.objects.get(id=id)
    patient.first_name = POST['first_name']
    patient.age = POST['age']
    patient.mobile = POST['mobile']
    patient.id_number = POST['id_number']
    patient.gender = POST['gender']
    patient.description = POST['description']
    patient.save()

def roles():
    return Role.objects.all()

def remove_patient(POST):
    patient = Patient.objects.get(id=POST['patient_id'])
    patient.delete()
