from django.http import HttpResponseForbidden
from .models import UserProfile, STUDENT

def student_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        try:
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.role == STUDENT:
                return function(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            pass
        return HttpResponseForbidden("You are not authorized to perform this action.")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
