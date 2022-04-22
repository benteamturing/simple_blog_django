from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounts.views import SignupView, UserListView
from posts.views import PostLatestListView, PostProfileListView, PostDetailView, PostCreateView
from profiles.views import ProfileDetailView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/signup/', SignupView.as_view(), name='signup'),
    # token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/users/', UserListView.as_view()),

    # profile
    path('api/profile/<int:pk>/', ProfileDetailView.as_view()),

    # post
    path('api/post/', PostCreateView.as_view()),
    path('api/post/<int:pk>', PostDetailView.as_view()),
    # posts
    path('api/posts/', PostLatestListView.as_view()),
    path('api/posts/<int:pk>', PostProfileListView.as_view()),
]