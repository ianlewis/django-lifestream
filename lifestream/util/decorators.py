#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

from django.http import HttpResponseNotAllowed

def allow_methods(*method_list):
    """
    Checks the request method is in one of the given methods
    """
    def _func(func):
        def __func(request, *argv, **kwargv):
            methods = method_list
            if "GET" in methods:
                methods += ("HEAD",)
            if request.method in methods:
                return func(request, *argv, **kwargv)
            return HttpResponseNotAllowed(methods)
        return __func
    return _func
