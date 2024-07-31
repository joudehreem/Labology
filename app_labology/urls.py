from django.urls import path
from . import views
urlpatterns = [
    path('1', views.error),
    path('2', views.about),
    path('3', views.all_patients),
    path('4', views.all_tests),
    path('5', views.patient),
    path('6', views.index),
    path('7', views.new_patient),

]


