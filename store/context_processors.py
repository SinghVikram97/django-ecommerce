# Create a file named context_processors.py in your app
from .models import UserProfile

def user_profile(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass
    return {'user_profile': profile}
