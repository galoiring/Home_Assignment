
from django.urls import path
from .views import WriteMessageView
from .views import UserMessagesView


urlpatterns = [
    path('api/write/', WriteMessageView.as_view(), name='api-write-message'),
    path('<str:username>/', UserMessagesView.as_view(), name='api-write-message'),



]
