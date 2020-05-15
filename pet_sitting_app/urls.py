from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('pets/', views.PetListView.as_view(), name='pet_list'),
    path('pets/<int:pet_id>/', views.PetDetailView.as_view(), name='pet_detail'),
    path('calendar/', views.AppointmentListView.as_view(), name='appointment_list'),
]
