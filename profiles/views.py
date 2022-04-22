from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileDetailView(APIView):
    http_method_names = ['GET', 'PUT', 'DELETE']

    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Profile.active_objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get_user_object(self, pk):
        try:
            return get_user_model().objects.get(profile=pk)
        except get_user_model().DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            profile = self.get_object(pk)
            serializer = ProfileSerializer(profile)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

    def delete(self, request, pk, format=None):
        try:
            user = self.get_user_object(pk)
            user.is_active = False
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)



