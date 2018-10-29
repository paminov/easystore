#from botocore.errorfactory import InvalidPasswordException
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView
from django.views.decorators.cache import never_cache
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django_warrant.backend import CognitoBackend
from .forms import RegisterForm, UserVerifyForm
from .models import Files
from .helpers import get_cognito_user_details
import pdb


def health(request):
    return JsonResponse('all is well', safe=False)


class BaseView(LoginRequiredMixin, TemplateView):

    def verify_logged_in(self, request):
        if not request.COOKIES.get('token'):
            return redirect()


class Home(LoginRequiredMixin, CreateView):

    template_name = 'home.html'
    model = Files
    fields = ['file', 'description', 'userid']
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        user_details = get_cognito_user_details(request.session)
        request.POST._mutable = True
        request.POST['userid'] = user_details['sub']
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            documents = Files.objects.all()
        else:
            user_details = get_cognito_user_details(self.request.session)
            documents = Files.objects.filter(userid=user_details['sub'])
        context['documents'] = documents
        return context


class Delete(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        file_obj = Files.objects.get(id=request.GET['id'])
        resp = file_obj.delete()
        return JsonResponse(resp[-1])


class Contents(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        file_obj = Files.objects.get(id=request.GET['id'])
        content = b"\n".join(file_obj.file.readlines())
        return JsonResponse({'content': content.decode('utf-8') })

    def post(self, request, *args, **kwargs):
        file_obj = Files.objects.get(id=request.POST['id'])
        wr_obj = file_obj.file.open(mode='w')
        response = wr_obj.write(request.POST['contents'])
        wr_obj.close()
        return JsonResponse({'response': response})


class Logout(LogoutView):

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        request.session.delete()
        return super().dispatch(request, *args, **kwargs)


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
