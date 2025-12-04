from django.urls import path
from . import views
from .api import check_availability, reserve_room

urlpatterns = [
    # -------- API для GigaChat --------
    path('api/check/', check_availability, name='api_check_availability'),
    path('api/reserve/', reserve_room, name='api_reserve_room'),

    # -------- Существующие маршруты --------
    path('modd', views.Moddview.as_view(), name="modd"),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('reservations/', views.ReservationListView.as_view(), name='reservation_list'),
    path('reservation/create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('reservation/<int:pk>/update', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('reservation/<int:pk>', views.ReservationDetailView.as_view(), name='reservation_detail'),
]
