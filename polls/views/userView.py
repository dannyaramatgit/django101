from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from ..forms import  UserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required()
def register(request):
    if request.method=='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['username'] = form.cleaned_data['username']
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return HttpResponseRedirect(reverse('polls:register'))
    else:
        form = UserForm()
        return render(request=request, template_name="polls/registration.html", context={'form':form})

class LogInUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request=request, template_name="polls/login.html", context={'form':form})

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return HttpResponseRedirect(reverse('polls:index'))
        else:
            return HttpResponseRedirect(reverse('polls:login'))



def logUserOut(request):
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse('polls:login'))
