from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class BaseView(TemplateView):

    def verify_logged_in(self, request):
        if not request.COOKIES.get('token'):
            return redirect()


class Home(TemplateView):

    def get(self, request, **kwargs):
        return render(request, 'base.html', context=None)


class Upload(TemplateView):

    def post(self, request, **kwargs):
        import pdb; pdb.set_trace()
        pass


class Contents(TemplateView):

    def get(self, request, **kwargs):
        pass
