from django.shortcuts import render

# Create your views here.
def error(request):
  return render(request,'404.html')
def about(request):
  return render(request,'about.html')
def all_patients(request):
  return render(request,'all_patients.html')
def all_tests(request):
  return render(request,'all_tests.html')
def patient(request):
  return render(request,'patient.html')
def index(request):
  return render(request,'login.html')
def new_patient(request):
  return render(request,'new_patient.html')