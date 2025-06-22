from django.contrib.auth.backends import BaseBackend
from .models import Player

class PlayerAuthBackend(BaseBackend):
    def authenticate(self, request, nickname=None, password=None):
        try:
            player = Player.objects.get(nickname=nickname)
            if player.check_password(password):
                return player
            return None
        except Player.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Player.objects.get(pk=user_id)
        except Player.DoesNotExist:
            return None