from django.urls import path
from .views import InitializePaymentView

urlpatterns = [
    path('initiate/', InitializePaymentView.as_view(), name='initiate-payment'),
]