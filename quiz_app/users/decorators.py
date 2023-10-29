from django.shortcuts import redirect, HttpResponseRedirect, Http404
from django.contrib import messages

def unautthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already logged in')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func