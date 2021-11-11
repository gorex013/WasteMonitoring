from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from waste_monitoring.forms import SignUpForm


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class SignupView(TemplateView):
    template_name = 'registration/signup.html'
    user_form = SignUpForm()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.user_form,
        }, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user_form = SignUpForm(request.POST)
        if self.user_form.is_valid():
            user = self.user_form.save(commit=False)
            user.email = self.user_form.data['username']
            user.save()
            return HttpResponse(status=301)
        return render(request, self.template_name, {
            'form': self.user_form,
        }, *args, **kwargs)
