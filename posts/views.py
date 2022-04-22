from django.http import Http404
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import IsOwnerOrReadOnly
from posts.models import Post
from posts.serializers import PostListSerializer, PostDetailSerializer


class PostCreateView(APIView):
    http_method_names = ['post']

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, *args, **kwargs):
        serializer = PostDetailSerializer(data=self.request.data)
        if serializer.is_valid():
            Post.objects.create(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})


class PostDetailView(APIView):
    http_method_names = ['GET', 'PUT', 'DELETE']

    permission_classes = (IsOwnerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Post.active_objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            post = self.get_object(pk)
            serializer = PostDetailSerializer(post)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})

    def delete(self, request, pk, format=None):
        try:
            post = self.get_object(pk)
            post.delete()
            return Response(status=status.HTTP_200_OK)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PostLatestListView(GenericAPIView, ListModelMixin):

    serializer_class = PostListSerializer

    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Post.active_objects.order_by('created')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProfilePostListView(GenericAPIView, ListModelMixin):

    serializer_class = PostListSerializer

    permission_classes = (permissions.AllowAny,)

    lookup_url_kwarg = 'profile_nickname'

    def get_queryset(self):
        return Post.objects.order_by('created')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
