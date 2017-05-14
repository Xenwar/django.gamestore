from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views import generic
from .models import Member
from gamecenter.models import State
from django.contrib.auth.models import Group
from django.http import Http404, HttpResponse, JsonResponse, \
    HttpResponseNotFound, HttpResponseRedirect
import json
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from hashlib import md5
from django.shortcuts import redirect
import uuid
from django.shortcuts import render
from django.core.urlresolvers import reverse

from django.contrib.auth import login,logout
from .forms import UserCreationForm, loginForm,ActivationForm,member_register
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)
#Not usable at the moment, 
#users cannot login unless activated the first time. 
#In the future, loggen should be allowed with limited capability. 
def is_not_active(user):
    active = user.is_active
    if active:
        return False
    else:
        return True #user is NOT active, How did the user logged in then ?

def user_is_not_loggen_in(user):
    if not user.is_authenticated():
        return True
    else:
        return False

def user_is_developer(user):
    return user.is_authenticated() and user.groups.filter(name='developers').exists()

def user_is_player(user):
    return user.is_authenticated() and user.groups.filter(name='players').exists()

class MemberListView(generic.ListView):
    model = Member
    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
            return self.model.objects.filter(groups__name='developers')
    template_name = 'members/developer_list.html'

class PlayerListView(generic.ListView):
    model = Member
    def get_context_data(self, **kwargs):
        context = super(PlayerListView, self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return self.model.objects.filter(groups__name='players')
    template_name = 'members/player_list.html'

'''
    context = {}
    messages = []
    messages.append("")
    context['messages'] = messages
    return render(
        request,
        'gamecenter/error.html',
        context,
    )
'''
#Authentication/Authorization related views

@user_passes_test(user_is_not_loggen_in,login_url="/")
def register(request):
        form = member_register(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("activation"))
        else:
            form = member_register()
            return render(request,"registration/register.html",{'form':form})

@user_passes_test(user_is_not_loggen_in,login_url="/")
def logging_in(request):
    form = loginForm(request.POST or None)
    if form.is_valid():
        email       = form.cleaned_data.get("email")
        user        = Member.objects.get(email = email)

        login(request, user)
        return HttpResponseRedirect("/")#show home page
    return render(request,"registration/login.html",{'form':form})
@csrf_exempt
@login_required
def logging_out(request):
    logout(request)
    return render(request,"registration/logout.html")
@csrf_exempt
@user_passes_test(is_not_active,login_url="/")
def activation(request):
    form = ActivationForm(request.POST or None)
    if form.is_valid():
        return HttpResponseRedirect("/")#show home page
    else:
        form = ActivationForm()
        return render(request,"registration/activate.html",{'form':form})
@csrf_exempt
def Calculating_the_checksum(request,pid,sid,secret_key,amount): #step 2 in the instruction, http://payments.webcourse.niksula.hut.fi/
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    logger.debug(checksum)
    return checksum