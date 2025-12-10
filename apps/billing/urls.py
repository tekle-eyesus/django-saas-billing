from django.urls import path
from .views import InitializePaymentView, ChapaWebhookView

urlpatterns = [
    path('initiate/', InitializePaymentView.as_view(), name='initiate-payment'),
    path('webhook/chapa/', ChapaWebhookView.as_view(), name='chapa-webhook'),
]