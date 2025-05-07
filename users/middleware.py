from django.utils import timezone
from django.core.cache import cache
from .models import User

class LastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            user_id = request.user.id
            cache_key = f'last_activity_{user_id}'
            if not cache.get(cache_key):
                User.objects.filter(id=user_id).update(last_activity=timezone.now())
                cache.set(cache_key, True, 60)
        return response