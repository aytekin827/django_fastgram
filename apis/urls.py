from django.urls import path, include
from apis.views import UserCreateView, UserLoginView, UserLogoutView, ContentCreateView, RelationCreateView, RelationDeleteView

urlpatterns = [
    path('v1/users/create/', UserCreateView.as_view(), name='apis_v1_user_create'),
    path('v1/users/login/', UserLoginView.as_view(), name='apis_v1_user_login'),
    path('v1/users/logout/', UserLogoutView.as_view(), name='apis_v1_user_logout'),

    path('v1/contents/create/', ContentCreateView.as_view(), name='apis_v1_content_create'),

    path('v1/relation/create/', RelationCreateView.as_view(), name='apis_v1_relation_create'),
    path('v1/relation/delete/', RelationDeleteView.as_view(), name='apis_v1_relation_delete'),
]
