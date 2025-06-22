from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from .models import Player, Item
from .forms import PlayerForm
def index(request):
    return render(request, 'index.html')

def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            if Player.objects.filter(nickname=form.cleaned_data['nickname']).exists():
                messages.error(request, 'Пользователей с таким ником уже зарегистрирован!')
                return render(request, 'registration.html', {'form': form})
            elif form.cleaned_data['password'] != form.cleaned_data['correct_password']:
                messages.error(request, 'Пароли не совпадают!')
                return render(request, 'registration.html', {'form': form})
            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('/login/')
        else:
            return render(request, 'registration.html', {"form": form})
    else:
        return render(request, 'registration.html', {'form':PlayerForm()})


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')

        player = authenticate(nickname=nickname, password=password)

        if player is not None:
            auth_login(request, player)
            return redirect('/game/')

        else:
            messages.error(request, 'Неверный логин или пароль')

    return render(request, 'login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def profile(request, player_id):
    player = request.user
    player.update_balance()
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'profile.html', {"player":player})

@login_required
def game(request):
    if request.method == 'POST':
        player = request.user
        player.clicks += 1
        player.money += player.money_per_click
        player.update_balance()
        player.save()
    return render(request, 'game.html')

@login_required
def shop(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        player = request.user
        buyer = player.buy_item(item_id)
        player.update_balance()

        #Проверка по первой букве на то, какое сообщение выводить
        if buyer[0][0] != "П":
            messages.error(request, buyer[0])
        else:
            messages.success(request, buyer[0])


    items = list(Item.objects.all())
    reg_items = items[:49]
    ult_item = items[49]
    items_table = [reg_items[i*7 : (i+1)*7] for i in range(7)]
    return render(request, 'shop.html', {
        'items_table':items_table,
        'ult_item':ult_item,
    })

@login_required
def leaderboard(request):
    player = request.user
    leaders = Player.objects.all().order_by('-clicks')[:100]
    full_lead = list(Player.objects.all().order_by('-clicks'))
    index_player = full_lead.index(player)
    return render(request, 'leaderboard.html', {"leaders":leaders, "player":player, "index_player":index_player})