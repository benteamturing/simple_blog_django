from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserListSerializer, SignupSerializer


class SignupView(APIView):
    http_method_names = ['post']

    permission_classes = (permissions.AllowAny,)

    def post(self, *args, **kwargs):
        serializer = SignupSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class UserListView(GenericAPIView, ListModelMixin):

    serializer_class = UserListSerializer

    def get_queryset(self):
        UserModel = get_user_model()
        return UserModel.active_objects.order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)