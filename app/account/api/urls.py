from django.urls import path
from account.api.views import RegistrationView, LoginView, UserActivityView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='api-registration'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('<int:user_id>/activity/', UserActivityView.as_view(), name='api-user-activity'),
]
