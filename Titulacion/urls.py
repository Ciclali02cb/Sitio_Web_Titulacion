from django.urls import path
from django.contrib.auth import views
from django.contrib.auth.views import LogoutView
from Titulacion import views 
from .views import custom_login



urlpatterns = [
    path('accounts/login/', custom_login, name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', views.home_view, name='home'),
    path('list', views.titulacion_list, name='titulacion_list'),
    path('new', views.create_titulacion, name='titulacion_new'),
    path('confirm', views.confirm_titulacion, name='confirm_titulacion'), 
    path('profesores', views.lista_profesores, name='lista_profesores'),
    path('agregar', views.agregar_profesor, name='agregar_profesor'),
    path('editar/<int:pk>/', views.update_titulacion, name='update_titulacion'),
    path('eliminar/<int:pk>/', views.delete_titulacion, name='delete_titulacion'),
    path('profesores/editar/<int:pk>/', views.update_profesor, name='update_profesor'),
    path('profesores/eliminar/<int:pk>/', views.delete_profesor, name='delete_profesor'),
    path('acta_Alumno/<int:pk>/', views.acta_Alumno, name='acta_Alumno'),
    path('guardar-acta/<int:pk>/', views.guardar_acta, name='Acta_guardar'),
]