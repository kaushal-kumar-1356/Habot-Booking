from django.urls import path
from . import views

urlpatterns = [
    path('bookings/', views.create_booking),
    path('bookings/list/', views.booking_list),
    path('bookings/<int:booking_id>/', views.booking_detail),
    path('lsas/search/', views.search_lsa),
    path('payments/', views.create_payment),
    path('payments/webhook/', views.payment_webhook),

]
