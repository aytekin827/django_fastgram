from django.urls import path, include
from apis.views import UserCreateView

urlpatterns = [
    path('v1/users/create/', UserCreateView.as_view(), name='apis_v1_user')
]