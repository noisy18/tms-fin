from django.utils.deprecation import MiddlewareMixin
from .context_processors import set_current_user, get_current_user

class CurrentUserMiddleware(MiddlewareMixin):
    # Middleware для сохранения текущего пользователя в промежуточное хранилище
    def process_request(self, request):
        set_current_user(request.user)