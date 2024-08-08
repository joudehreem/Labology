from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Create your views here.
def error(request):
  return render(request,'404.html')
def about(request):
  if 'user_id' not in request.session:
      return render(request,'about.html')
  else:
    context = {
      'provider': get_user(request.session),
  }
  return render(request,'about.html',context)
def all_patients(request):
  if 'user_id' not in request.session:
      return redirect('/')
  else:
    context={
        'provider':get_user(request.session),
        'patients':patients(),
        'tests':tests(),

        
      }
    return render(request,'all_patients.html',context)
  
def edit_patient(request, patient_id, test_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
      patient= get_patient(patient_id)
      test = get_test(patient, test_id)

      context = {
          'patient': patient,
          'provider': get_user(request.session),
          'test': test
      }
    return render(request, 'edit_patient.html', context)


def patient(request,id):
  if 'user_id' not in request.session:
    return redirect('/')
  else:
    context={
      'patient':Patient.objects.get(id=id),
      'provider':get_user(request.session)
    }
    return render(request,'patient.html',context)

def index(request): 
  if 'user_id' not in request.session:
    return render(request,'login.html')
  else:
    context={
        'provider':get_user(request.session),
        
      }
    return render(request,'login.html',context)

def new_patient(request):
  if 'user_id' not in request.session:
      return redirect('/')
  else:
    context={
        'provider':get_user(request.session),
        
      }
  return render(request,'new_patient.html',context)

#handel request POST to add user & validate
def register_user(request):
    if request.method == 'POST':
      errors = Provider.objects.basic_register(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():   
            messages.error(request, value)    
        return redirect('/')
    else:
      create_user(request.POST)
      messages.success(request, "Successfully Register")

      return redirect('/')

def login_user(request):
    if request.method == 'POST':
        errors = Provider.objects.basic_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        user = Provider.objects.filter(email=request.POST['email']) 
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password .encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/patients')
        else:
            messages.error(request, "Invalid password.")
            return redirect('/')
          

def register_patient(request):
  if request.method == 'POST':
    # if request.method == 'POST':
    #   errors = Provider.objects.basic_register(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():   
    #         messages.error(request, value)    
    #     return redirect('/')
    # else:
    create_patient(request.POST)
    return redirect('/patients')
  
def add_test(request,id):
  if request.method == 'POST':
    # patient=patient(id)
    crate_test(request.POST,id)
    return redirect(f'/patient/{id}')

# def add_result(request):
#   context = {
#         'patient': patient_instance,
#         'provider': get_user(request.session),
#         'test': test_instance
#     }
#   return render(request,'edit_patient.html',context)

def logout(request):
    if request.method=='POST':
        request.session.clear()
        return redirect('/')