#from botocore.errorfactory import InvalidPasswordException
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import TemplateView, FormView
from django.urls import reverse
from .forms import RegisterForm, UserVerifyForm
from .backend import CognitoBackend
import pdb


class BaseView(LoginRequiredMixin,TemplateView):

    def verify_logged_in(self, request):
        if not request.COOKIES.get('token'):
            return redirect()


class Home(LoginRequiredMixin,TemplateView):

    def get(self, request, **kwargs):
        return render(request, 'home.html', context=None)


class Upload(LoginRequiredMixin,TemplateView):

    def post(self, request, **kwargs):
        import pdb; pdb.set_trace()
        pass


class Contents(LoginRequiredMixin,TemplateView):

    def get(self, request, **kwargs):
        pass


class UserVerify(FormView):

    template_name = 'verify_user.html'
    form_class = UserVerifyForm

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.kwargs.get('username', '')
        return initial

    def get_success_url(self):
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):

        cognito = CognitoBackend()
        try:
            resp = cognito.validate_user(**form.cleaned_data)
        except Exception as e:
            pass
            # TODO: create proper response based on error
            #pdb.set_trace()

        return super().form_valid(form)


class Register(FormView):

    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):

        cognito = CognitoBackend()
        password_error = "Invalid Password. Password must contain "\
                     "numbers, uppercase,lowercase & special characters"
        user_exits_error = "Username is already in use."
        try:
            resp = cognito.register(**form.cleaned_data)
        except Exception as e:
            if "Password did not conform with policy" in str(e):
                form.errors['password'] = \
                                    form.error_class([password_error])
                return self.form_invalid(form)
            elif "User already exists" in str(e):
                form.errors['username'] = \
                                    form.error_class([user_exits_error])
                return self.form_invalid(form)
            else:
                raise(e)

        return HttpResponseRedirect(reverse('verify_user', 
                    kwargs={'username': form.cleaned_data['username']}))
        #return UserVerify.as_view(username=form.cleaned_data['username'])