from django.urls import path
from . import views

urlpatterns = [
    path('checkin-records/', views.checkin_records, name='checkin_records'),
    path('checkin/', views.check_in, name='check_in'),
    path('checkout/', views.check_out, name='check_out'),
    path('status/', views.staff_status, name='staff_status'),
    path('depot/checkin/', views.depot_checkin, name='depot_checkin'),
]