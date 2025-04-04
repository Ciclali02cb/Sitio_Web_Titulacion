from django.urls import path
from Titulacion import views


urlpatterns = [
    path('list', views.titulacion_list, name='titulacion_list'),
    path('new', views.create_titulacion, name='titulacion_new'),
    path('confirm', views.confirm_titulacion, name='confirm_titulacion'),   
    path('buscar', views.buscar_titulaciones, name='buscar_titulaciones'),
    path('profesores', views.lista_profesores, name='lista_profesores'),
    path('agregar', views.agregar_profesor, name='agregar_profesor'),
    path('editar/<int:pk>/', views.update_titulacion, name='update_titulacion'),
    path('eliminar/<int:pk>/', views.delete_titulacion, name='delete_titulacion'),
]