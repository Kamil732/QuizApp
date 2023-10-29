from math import ceil

from django.shortcuts import (
    render,
    HttpResponseRedirect,
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from django.views import generic
from django.contrib.auth import (
    login,
    logout,
    authenticate,
)

from quizes.models import Quiz

from .models import User
from . import forms

class LoginView(generic.FormView):
    template_name = 'users/login.html'
    form_class = forms.LoginUserForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        messages.success(self.request, 'You successfully have just loged in')

        next = self.request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('/')

class RegisterView(generic.CreateView):
    template_name = 'users/register.html'
    form_class = forms.RegisterUserForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        messages.success(self.request, f'You have successfully registered and logged into "{user}" account')

        next = self.request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('/')

class LogoutView(generic.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        message.success(request, 'You have successfully logged out')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class ProfileSettingsView(generic.FormView):
    template_name = 'users/profile_settings.html'

    def get_form(self):
        form = forms.MyProfileForm(self.request.POST, instance=self.request.user)
        if self.request.method == 'GET':
            form = forms.MyProfileForm(initial=self.get_initial())
        return form

    def get_initial(self, *args, **kwargs):
        user = self.request.user
        initial = super(ProfileSettingsView, self).get_initial(*args, **kwargs)

        initial['username'] = user.username
        initial['email'] = user.email
        initial['facebook'] = user.facebook
        initial['website'] = user.website
        initial['description'] = user.description

        if not(user.image_url == user.DEFAULT_IMAGE_URL):
            initial['image_url'] = user.image_url

        return initial

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile's settings has been successfully saved")
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))

class ProfileView(generic.DetailView):
    template_name = 'users/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(User, slug=slug)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        page = self.kwargs.get('page')

        context['quiz_sections'] = Quiz.SECTION
        context['quiz_categories'] = Quiz.CATEGORY

        quizes = Quiz.objects.filter(author=self.get_object(), is_published='True')
        context['quizes'] = quizes[page*10-10:page*10]
        context['page_items'] = ceil(quizes.count()/10)

        return context