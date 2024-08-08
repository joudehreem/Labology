from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register_user',views.register_user),
    path('login_user',views.login_user),

    path('patients', views.all_patients),

    path('1', views.error),
    path('about', views.about),
    path('patient/<int:id>/', views.patient),
    path('new_patient', views.new_patient),
    path('register_patient',views.register_patient),
    path('patient/<int:id>/add_test/',views.add_test),
    path('patient/<int:patient_id>/update_test/<int:test_id>', views.edit_patient, name='update_test'),
    path('logout',views.logout)


]


