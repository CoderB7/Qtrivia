from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (CustomPasswordResetView, CustomPasswordChangeView,
                    CustomLoginView, logout, register, CustomPasswordResetCompleteView,
                    CustomPasswordResetDoneView, edit
                    )
from .forms import CustomSetPasswordForm


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('profile/', edit, name='profile'),

    # change password urls
    path('password_change/',
         CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='account/password_change_done.html'
         ),
         name='password_change_done'),

    # reset password urls
    path('password-reset/',
         CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html',
             form_class=CustomSetPasswordForm,
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]

