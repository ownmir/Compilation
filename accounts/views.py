from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm  # add emeil
from django.contrib.auth import login as auth_login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('two_factor:profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user


# def password_reset_complete(request):
#     return render(request, 'accounts/password_reset_done.html')


def password_change_done(request):
    return render(request, 'accounts/password_change_done.html')
