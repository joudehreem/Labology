from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.http import HttpResponse

# Create your views here.

# render to error handling page
def error(request):
  return render(request,'404.html')

#render about page
def about(request):
  if 'user_id' not in request.session:
      return render(request,'about.html')
  else:
    context = {
      'provider': get_user(request.session),
  }
  return render(request,'about.html',context)

# render to login and registration page and if user go to the login page clear session
def home(request):
  request.session.clear()

  context={
            'roles': Role.objects.all(),
          }
  return render(request, 'login.html', context)

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
    
# handel request POST to login user and redirect to the main page
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
    return redirect('/1')
  
# handel request POST to register user and redirect to the login page
def register_patient(request):
  if request.method == 'POST':
    #   errors = Provider.objects.basic_register(request.POST)
    # if len(errors) > 0:
    #     for key, value in errors.items():   
    #         messages.error(request, value)    
    #     return redirect('/')
    # else:
      patient =create_patient(request.POST)  
      provider = request.session.get('user_id')  
      provider = Provider.objects.get(id=provider)
      patient.episodes.add(provider)     
      return redirect('/patients')
  
# render page to retrave for all patients data and  pagination in the page
def all_patients(request):
  if 'user_id' not in request.session:
      return redirect('/')
  else:
    if 'query' in request.GET:
      query=request.GET['query']
      patients_list=Patient.objects.filter(first_name__icontains=query)
    else:
      patients_list=patients()
    paginator = Paginator(patients_list, 5) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context={
        'provider':get_user(request.session),
        'tests':tests(),
        'patients_list':patients_list,
        'page_obj':page_obj
      }
    return render(request,'all_patients.html',context)

# page to view all details in patient profile and add test 
def patient(request, id):
  if 'user_id' not in request.session:
        return redirect('/')
  else:
    patient = get_patient(id)
    patient_tests = PatientTest.objects.filter(patient=patient)
    paginator = Paginator(patient_tests, 5)  # Show 5 tests per page
    page_number = request.GET.get("page")  # Get current page number from request
    page_obj = paginator.get_page(page_number)  # Get the tests for the current page
    context = {
        'patient': patient,
        'provider': get_user(request.session), 
        'page_obj': page_obj,
        'tests': tests(),   
        'tests_list':patient_tests
        
    }
  return render(request, 'patient.html', context)

# edit patient's 
def edit_patient(request, patient_id, test_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    patient = get_patient(patient_id)
    test = PatientTest.objects.get(id=test_id, patient=patient)
    context = {
        'patient': patient,
        'test': test,
        'provider': get_user(request.session),
        'patient_tests': PatientTest.objects.filter(patient=patient_id),
    }

    return render(request, 'edit_patient.html', context)

# page to add a new patient
def new_patient(request):
  if 'user_id' not in request.session:
      return redirect('/')
  else:
    context={
        'provider':get_user(request.session),
        'patient':Patient.objects.all()
        }
    return render(request,'new_patient.html',context)



#add test to the patient
def add_test(request, id):
  if request.method == 'POST':
    # patient=patient(id)
    create_test(request.POST,id)
    return redirect(f'/patient/{id}')

# add result to the test
def add_result(request,id):
  if request.method == 'POST':
    update_test(request.POST,id)
    
    return redirect(f'/patients')

# clear the user seesion
def logout(request):
    if request.method=='POST':
        request.session.clear()
        return redirect('/')

#delete the file of patient
def delete(request):
  if request.method =='POST':
    remove_patient(request.POST)
    return redirect('/patients')

# generate to pdf
def generate_pdf(request, id):
    try:
        # Retrieve the PatientTest object
        test = PatientTest.objects.get(id=id)
    except PatientTest.DoesNotExist:
        return HttpResponse("PatientTest not found.", status=404)
    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Draw the patient and test information onto the PDF
    p.drawString(100, height - 100, f"Patient Name: {test.patient.first_name} {test.patient.last_name}")
    p.drawString(100, height - 120, f"Type of Test: {test.test.type_of_test}")
    p.drawString(100, height - 140, f"Test Result: {test.test_result}")


    # Finalize the PDF file
    p.showPage()
    p.save()

    # Move the buffer position to the beginning
    buffer.seek(0)

    # Return the PDF file as an HTTP response
    return HttpResponse(buffer, content_type='application/pdf')
