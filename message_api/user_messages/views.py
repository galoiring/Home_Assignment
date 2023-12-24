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
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserMessagesView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        messages = Message.objects.filter(receiver=user)
        data = {'messages': [{'sender': message.sender.username,
                              'subject': message.subject, 'message': message.message} for message in messages]}
        return JsonResponse(data)
