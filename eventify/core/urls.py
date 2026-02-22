from django.urls import path
from .views import DashboardView, UserEndPoints, UserManagementView, ViewUser

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('user/api/v1/getUsers/', UserEndPoints.as_view(), name='get_users'),
    path('user/management/', UserManagementView.as_view(), name='user_management'),
    path('user/view/<uuid:uuid>/', ViewUser.as_view(), name='view_user'),
]