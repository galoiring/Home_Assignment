from django.urls import path
from .views import WriteMessageView, UserMessagesView, UnreadUserMessagesView, ReadMessageView, DeleteMessageView

urlpatterns = [
    path('api/write/', WriteMessageView.as_view(), name='api-write-message'),
    path('<str:username>/', UserMessagesView.as_view(), name='user-messages'),
    path('<str:username>/unread/',
         UnreadUserMessagesView.as_view(), name='unread-messages'),
    path('<str:username>/read/', ReadMessageView.as_view(), name='read-message'),
    path('api/delete/<int:message_id>/',
         DeleteMessageView.as_view(), name='api-delete-message'),



]
