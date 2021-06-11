from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, RedirectView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from user.forms import SignInForm, SignUpForm

# Create your views here.
from user.models import UserProfile


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "registration/sign-up.html"
    success_url = reverse_lazy('user:sign-in')


class SignInView(LoginView):
    form_class = SignInForm
    template_name = "registration/sign-in.html"

    def get_success_url(self):
        return reverse_lazy('store:list')


class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('store:list')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfileView(TemplateView):
    """User profile view implementation"""

    template_name = "registration/profile.html"

    def get_context_data(self):
        """Return a context data dictionary"""

        user = self.request.user
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = None

        return {"user": user, "profile": profile}
