from django.urls import path

from user.views import LogoutView, SignUpView, SignInView, UserProfileView

app_name = 'user'
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
