from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('home',views.home),
    path('register_user',views.register_user),
    path('login_user',views.login_user),
    path('update_new_patient/<int:id>/',views.update_new_patient),
    path('patients', views.all_patients),
    path('update_patient/<int:id>',views.update_patient),
    path('1', views.error),
    path('about', views.about),
    path('patient/<int:id>/', views.patient),
    path('new_patient', views.new_patient),
    path('register_patient/',views.register_patient),
    path('update_test/<int:patient_id>/<int:test_id>/', views.edit_patient, name='update_test'),
    path('logout',views.logout),
    path('pdf/<int:id>/', views.generate_pdf, name='generate_pdf'),
    path('<int:id>/add_result', views.add_result),
    path('add_test/<int:id>',views.add_test),
    path('delete', views.delete)

    
]


