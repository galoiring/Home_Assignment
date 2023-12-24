from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from django.http import JsonResponse


class WriteMessageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error',
                         'errors': serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class UserMessagesView(APIView):
    def get(self, request):
        # user = get_object_or_404(User, username=username)
        if request.user.is_anonymous:
            default_user, created = User.objects.get_or_create(
                username='gal')
            request.user = default_user

        user = request.user
        messages = Message.objects.filter(receiver=user)

        response = {'messages': [{'sender': message.sender.username,
                                  'reciver': message.receiver.username,
                                  'subject': message.subject,
                                  'message': message.message,
                                  'message_id': message.message_id,
                                  'is_read': message.is_read,
                                  } for message in messages]}
        return JsonResponse(response)


class UnreadUserMessagesView(UserMessagesView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        messages = Message.objects.filter(receiver=user, is_read=False)

        response = {'messages': [{'sender': message.sender.username,
                                  'subject': message.subject,
                                  'message': message.message,
                                  'message_id': message.message_id,
                                  'is_read': message.is_read,
                                  } for message in messages]}
        return JsonResponse(response)


class ReadMessageView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        last_unread_message = Message.objects.filter(
            receiver=user, is_read=False).last()

        if last_unread_message:
            last_unread_message.is_read = True
            last_unread_message.save()

            response = {'message': {'sender': last_unread_message.sender.username,
                                    'reciver': last_unread_message.receiver.username,
                                    'subject': last_unread_message.subject,
                                    'message': last_unread_message.message,
                                    'is_read': last_unread_message.is_read,
                                    'message_id': last_unread_message.message_id
                                    }}
            return JsonResponse(response)

        return Response({'detail': 'No unread messages found.'}, status=status.HTTP_404_NOT_FOUND)


class DeleteMessageView(APIView):
    def delete(self, request, message_id, *args, **kwargs):
        message = get_object_or_404(Message, message_id=message_id)

        if request.user == message.sender or request.user == message.receiver:
            message.delete()
            return Response({'status': 'success'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': 'error', 'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
