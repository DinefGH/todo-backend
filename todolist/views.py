from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from todolist.models import TodoItem
from todolist.serializers import TodoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import date
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
import logging
# Create your views here.


class TodoItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        todos =  TodoItem.objects.filter(author=request.user)
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TodoItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # 'author' and 'created_at' are set in the serializer's create method
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk, format=None):
        todo = TodoItem.objects.filter(pk=pk, author=request.user).first()
        if todo:
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TodoItemDetailView(APIView):
    
    """
    Retrieve, update or delete a todo item instance.
    """
    def get_object(self, pk, user):
        return get_object_or_404(TodoItem, pk=pk, author=user)

    def delete(self, request, pk, format=None):
        logger = logging.getLogger(__name__)
        logger.debug(f"Attempting to delete TodoItem {pk} by user {request.user}")
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        todo_item = self.get_object(pk, request.user)
        todo_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
        context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })