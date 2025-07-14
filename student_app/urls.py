from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('export/', views.export_students_csv, name='export_students_csv'),
    path('import/', views.import_csv, name='import_csv'),
    path('dashboard/', views.dashboard, name='dashboard'),
]