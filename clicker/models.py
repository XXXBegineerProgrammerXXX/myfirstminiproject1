from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class PlayerManager(BaseUserManager):
    def create_user(self, nickname, password=None, **extra_fields):
        if not nickname:
            raise ValueError('The Nickname must be set')
        player = self.model(nickname=nickname, **extra_fields)
        player.set_password(password)
        player.save()
        return player


class Item(models.Model):
    title = models.CharField(max_length=128, unique=True)
    price = models.IntegerField()
    money_per_click = models.IntegerField(default=0)
    money_per_sec = models.IntegerField(default=0)

    class Meta:
        ordering = ['price', 'title']

    def __str__(self):
        return self.title


class Purchase(models.Model):
    player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='purchases')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['player', 'item']]


class Player(AbstractBaseUser):
    nickname = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)
    money = models.IntegerField(blank=True, default=0)
    money_per_click = models.IntegerField(blank=True, default=1)
    money_per_sec = models.IntegerField(blank=True, default=0)
    last_update = models.DateTimeField(auto_now=True)
    clicks = models.IntegerField(default=0)

    objects = PlayerManager()

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = []  # Добавляем обязательный атрибут

    def update_balance(self):
        now = timezone.now()
        delta_seconds = (now - self.last_update).total_seconds()
        balance = self.money_per_sec * delta_seconds
        self.money += int(round(balance))
        self.last_update = now
        self.save()

    def buy_item(self, item_id):
        item = Item.objects.get(id=item_id)

        if self.purchases.filter(item=item).exists():
            return ["Этот предмет уже куплен!"]

        elif self.money < item.price:
            return ["Недостаточно средств!"]

        Purchase.objects.create(player=self, item=item)
        self.money -= item.price
        self.money_per_click += item.money_per_click
        self.money_per_sec += item.money_per_sec
        self.save()

        return ["Покупка прошла успешно!"]



    def set_password(self, raw_password):
        raw_password = make_password(raw_password)
        #Можно хэшировать и несколько раз, но для этого нужен мощный сервер
        self.password = raw_password

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.nickname
