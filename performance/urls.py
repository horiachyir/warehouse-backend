from django.urls import path
from . import views

urlpatterns = [
    path('metrics/', views.PerformanceMetricListView.as_view(), name='performance_metrics'),
    path('dashboard/', views.current_dashboard_data, name='current_dashboard_data'),
    path('dashboard-data/', views.DashboardDataListView.as_view(), name='dashboard_data_list'),
    path('staff-locations/', views.StaffLocationListView.as_view(), name='staff_locations'),
    path('update-location/', views.update_staff_location, name='update_staff_location'),
    path('staff-in-depot/', views.staff_in_depot, name='staff_in_depot'),
]