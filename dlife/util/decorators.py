#!/usr/bin/env python
#:coding=utf-8:
#:tabSize=2:indentSize=2:noTabs=true:
#:folding=explicit:collapseFolds=1:

def allow_methods(*methods):
    def _func(func):
        def __func(request, *argv, **kwargv):
            if request.method in methods:
                return func(request, *argv, **kwargv)
            return HttpResponseNotAllowed(methods)
        return __func
    return _func