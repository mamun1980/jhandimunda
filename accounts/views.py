# from typing import Any
# from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from typing import Any
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import Group
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView

from .forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from .serializers import UserSerializer, GroupSerializer, RegisterSerializer

from apps.wallet.models import Wallet
from apps.game.models import Player, Agent

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserRegistrationView(CreateView):
    template_name = 'accounts/auth-signup.html'
    form_class = RegistrationForm
    success_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        want_to_agent = request.POST.get('want_to_agent')
        form = self.get_form()
        if form.is_valid():
            try:
                user = form.save()
                wallet = Wallet.objects.create(user=user)
                if want_to_agent == 'on':
                    user.is_agent = True
                    agent = Agent.objects.create(user=user)
                else:
                    user.is_player = True
                    player = Player.objects.create(user=user)
                user.save()
                return HttpResponseRedirect("/accounts/login/")
            except Exception as e:
                print(e)
                pass
        
        else:
            return self.form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/auth-signin.html'
    form_class = LoginForm
    succes_url = '/'

    def post(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return HttpResponseRedirect("/admin/")
                
            # elif user.is_agent:
            #     return HttpResponseRedirect("/agents/")
            # elif user.is_player:
            #     return HttpResponseRedirect("/players/")                
            else:
                return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/accounts/login/")


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/auth-reset-password.html'
    form_class = UserPasswordResetForm


class UserPasswrodResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/auth-password-reset-confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/auth-change-password.html'
    form_class = UserPasswordChangeForm


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


@login_required(login_url='/accounts/login/')
def profile(request):
    context = {
        'segment': 'profile',
    }
    return render(request, 'accounts/profile.html', context)

