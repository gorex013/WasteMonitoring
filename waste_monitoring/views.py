from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from waste_monitoring.forms import SignUpForm, DataIntroductionForm


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
            return redirect(to='login', *args, **kwargs)
        return render(request, self.template_name, {
            'user_form': self.user_form,
        }, *args, **kwargs)


class ShowGraphView(TemplateView):
    template_name = 'data-display/data-display.html'

    def get(self, request, *args, **kwargs):
        type_id = kwargs['type_id']
        if type_id not in ['plastic', 'metal-sticla', 'bio']:
            return redirect('home')
        if type_id == 'plastic':
            type_name = type_id.title()
            image = 'plastic.jpg'
        elif type_id == 'metal-sticla':
            type_name = 'Metal/Sticlă'
            image = 'metal-sticla.jpg'
        elif type_id == 'bio':
            type_name = 'Biodegradabil'
            image = 'biodegradabile.jpg'
        else:
            type_name = 'No name'
            image = ''
        return self.render_to_response(
            {
                'title': 'Table View',
                'data': [
                    ['Column1', 'Column2', 'Column3'],
                    [1, 2, 4],
                    [3, 4, 24]
                ],
                'type_name': type_name,
                'image': image
            })


class ChooseGraphTypeView(TemplateView):
    template_name = 'data-display/show-graph.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class InsertDataView(TemplateView):
    template_name = 'data-insert-form.html'
    waste_form = DataIntroductionForm()

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # login = reverse(LoginView)
            # print(login)
            # return LoginView.as_view(context={'login_message': 'Trebui să fii logat ca să poți introduce date!'})
            return redirect('login')
        # if has_permission  request.user
        return self.render_to_response({'form': self.waste_form})

    def post(self, request, *args, **kwargs):
        self.waste_form = DataIntroductionForm(request.POST)
        if self.waste_form.is_valid():
            data = self.waste_form.save(commit=False)
            data.user_id = request.user.id
            data.save()
            self.waste_form = DataIntroductionForm()
            return self.render_to_response(
                {'message': 'Datele au fost introduse cu succes!', 'type': 'success', 'form': self.waste_form})
        return self.render_to_response({'form': self.waste_form})
