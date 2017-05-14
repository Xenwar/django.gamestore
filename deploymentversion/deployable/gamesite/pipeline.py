from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views import generic
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
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
import logging
def addToGroup(backend, response, user, *args, **kwargs):
    if user is not None:
        if backend.name == "facebook":
            group = Group.objects.get(name="players")
            user.groups.add(group)
                #return user
        else:
            raise ValueError()