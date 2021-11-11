from django.shortcuts import render, redirect
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
            'user_form': self.user_form,
        }, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user_form = SignUpForm(request.POST)
        if self.user_form.is_valid():
            user = self.user_form.save(commit=False)
            user.email = self.user_form.data['username']
            user.save()
            return redirect(request=request, to='login', *args, **kwargs)
        return render(request, self.template_name, {
            'user_form': self.user_form,
        }, *args, **kwargs)
