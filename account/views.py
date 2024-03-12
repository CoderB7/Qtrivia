from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                       PasswordResetView, PasswordResetDoneView,
                                       PasswordResetCompleteView)
from .forms import (LoginForm, UserRegistrationForm, CustomPasswordChangeForm, CustomPasswordResetForm,
                    CustomSetPasswordForm, UserEditForm, ProfileEditForm)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from quiz.models import Quiz


class CustomPasswordResetCompleteView(LoginRequiredMixin, PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

    def get(self, request, *args, **kwargs):
        context = locals()
        context['is_reset_page'] = True
        return render(request, self.template_name, context)


class CustomPasswordResetDoneView(LoginRequiredMixin, PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
    is_reset_done_page = True

    def get(self, request, *args, **kwargs):
        context = locals()
        context['is_reset_page'] = True
        return render(request, self.template_name, context)


class CustomPasswordResetView(PasswordResetView):
    form = CustomPasswordResetForm
    template_name = 'account/password_reset_form.html'  # Provide your custom template
    email_template_name = "account/password_reset_email.html"
    is_reset_page = True

    def get(self, request, *args, **kwargs):
        context = locals()
        context['form'] = self.form
        context['is_reset_page'] = True
        context['email_template_name'] = self.subject_template_name
        return render(request, self.template_name, context)


class CustomPasswordChangeView(PasswordChangeView):
    form = CustomPasswordChangeForm
    template_name = "account/password_change_form.html"


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = LoginForm
    next_page = 'quiz_list'
    is_auth_page = True

    def get(self, request, *args, **kwargs):
        context = locals()
        context['form'] = self.authentication_form
        context['is_auth_page'] = self.is_auth_page
        context['next_page'] = self.next_page
        return render(request, self.template_name, context)


def logout(request):
    if request.method == 'GET':
        django_logout(request)
        return render(request, 'account/logout.html')


def register(request):
    is_auth_page = True
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, "Your account has been created! You are now able to login")
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {'user_form': user_form, 'is_auth_page': is_auth_page})


@login_required
def edit(request):
    user_quizzes = Quiz.objects.filter(user=request.user).order_by('-solved').all()
    user_quizzes_amount = len(user_quizzes)
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
        return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'user_quizzes': user_quizzes_amount})
