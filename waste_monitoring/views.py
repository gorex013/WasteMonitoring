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
