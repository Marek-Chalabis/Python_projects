from django.shortcuts import render, redirect
from .forms import AvatarCreation, LvlUp
from .models import Hero, Beast
from .logic import rules, create_enemy
from django.contrib import messages
import random


def war_greetings(request):
    # greetings view
    player = 'Input your name'
    if request.method == "POST":
        player = request.POST.get("player")
        try:
            # checks if the player exists
            avatar = Hero.objects.get(name=player)
            enemy = avatar.beast_set.last()
            return redirect('battle', beast_id=enemy.id, avatar_id=avatar.id)
        except:
            player = f'{player} doesn\'t exists'
    return render(request, 'greetings.html', {'player': player})


def create_avatar(request):
    # creates new avatar
    form = AvatarCreation(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            # adds bonus stat depends on race
            race = form.cleaned_data.get('race')

            if race == 'human':
                DMG = form.cleaned_data.get('DMG')
                form.instance.DMG = DMG + 5
            elif race == 'elf':
                DEX = form.cleaned_data.get('DEX')
                form.instance.DEX = DEX + 5
            elif race == 'orc':
                DEF = form.cleaned_data.get('DEF')
                form.instance.DEF = DEF + 5

            form.instance.LVL = 1
            # random starting HP
            form.instance.HP = random.randint(80, 120)
            form.save()
            avatar = form.save()
            # creates enemy
            enemy = create_enemy(avatar)
            enemy.save()
            return redirect('battle', beast_id=enemy.id, avatar_id=avatar.id)
    else:
        form = AvatarCreation()

    return render(request, 'avatar.html', {'form': form})


def battle(request, beast_id, avatar_id):
    enemy = Beast.objects.get(id=beast_id)
    avatar = Hero.objects.get(id=avatar_id)
    # checks for cheats
    cheat = False

    avatar_before_fight = avatar.HP
    enemy_before_fight = enemy.HP

    # creates course of battle
    battle_info = rules(avatar, enemy)

    if str(Beast.objects.get(id=beast_id).opponent) != avatar.name:
        # this will unable user to fight other users beasts
        cheat = True

    context = {
        'avatar': avatar,
        'avatar_before_fight': avatar_before_fight,
        'enemy': enemy,
        "enemy_before_fight": enemy_before_fight,
        'battle_info': battle_info,
        'cheat': cheat
    }
    return render(request, 'battle.html', context)


def rest(request, beast_id, avatar_id):
    avatar = Hero.objects.get(id=avatar_id)
    # distribute one point from lvl up
    form = LvlUp(request.POST)
    # blocks refreshes on web to gain more points and HP
    no_cheat = True

    try:
        if request.method == 'POST':
            if form.is_valid():
                stat = form.cleaned_data.get('stat')
                # checks if the beast "belonged" to player
                if str(Beast.objects.get(id=beast_id).opponent) == str(avatar.name):
                    if stat != None:
                        if stat == 'DMG':
                            avatar.DMG += 1
                        elif stat == 'DEF':
                            avatar.DEF += 1
                        elif stat == 'DEX':
                            avatar.DEX += 1
                        # regenerate HP and lvl UP
                        hp_regenerate = random.randint(0, 50)
                        avatar.HP += hp_regenerate
                        avatar.LVL += 1
                        avatar.save()
                        # deletes defeated beast, that gave a experience
                        Beast.objects.filter(id=beast_id).delete()
                        # creates new enemy
                        enemy = create_enemy(avatar)
                        enemy.save()
                        messages.info(request, f'{avatar.name} regenerated {hp_regenerate} HP')

                    return redirect('battle', beast_id=enemy.id, avatar_id=avatar.id)
                else:
                    no_cheat = False
    except:
        no_cheat = False

    context = {
        'avatar': avatar,
        'no_cheat': no_cheat,
        'form': form,
    }
    return render(request, 'rest.html', context)


def summary(request, avatar_id):
    avatar = Hero.objects.get(id=avatar_id)
    context = {
        'avatar': avatar,

    }
    avatar.delete()
    return render(request, 'summary.html', context)
