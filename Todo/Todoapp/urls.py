

from django.urls import path

from Todoapp.views import *

urlpatterns = [
    path('', Todo_item_view.as_view()),
    path('user-register/', UserRegisterAPIView . as_view()),
    path('user-login/', LoginAPIView . as_view()),
    path('user-logout/', LogoutAPIView . as_view()),
]