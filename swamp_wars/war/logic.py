import random
from .models import Beast


def create_enemy(avatar):
    enemy = Beast(
        name=random.choice(['Abhoth', 'Daoloth', 'Nyctelios', 'Suc\'Naath', 'Yad-Thaddag', 'Oryx']),
        DMG=(random.randint(1, 10) + random.randint(0, avatar.LVL)),
        DEX=(random.randint(1, 10) + random.randint(0, avatar.LVL)),
        DEF=(random.randint(1, 10) + random.randint(0, avatar.LVL)),
        HP=(random.randint(50, 150) + random.randint(0, (2 * avatar.LVL))),
        race=random.choice(['Goblin', 'Demon', 'Troll', 'Naga']),
        opponent=avatar)
    return enemy


def versus(attacker, blocker):
    if blocker.DEX * 3 < random.randint(0, 100):
        if attacker.DMG <= blocker.DEF or attacker.DMG * 2 <= blocker.DEF:
            blocker.HP -= 1
            action = 'doing only 1 damage because enemy armor is bigger then his attack'
        else:
            if attacker.DEX * 2 > random.randint(0, 100):
                action = f'CRITICALLY striking opponent for {(attacker.DMG * 2 - blocker.DEF)} damage'
                blocker.HP = blocker.HP - (attacker.DMG * 2 - blocker.DEF)
            else:
                action = f'striking opponent for {attacker.DMG - blocker.DEF} damage'
                blocker.HP = blocker.HP - (attacker.DMG - blocker.DEF)
    else:
        blocker.HP = blocker.HP - int(attacker.DMG * 0.1)
        action = f'{attacker.name} misses, {blocker.name} taking only 10% normal DMG: {int(attacker.DMG * 0.1)}'

    blocker.save()
    return action


def rules(avatar, enemy):
    turn = random.randint(0, 1)
    if turn == 0:
        action_first = versus(avatar, enemy)
        first_attack = avatar
        action_second = versus(enemy, avatar)
        second_attack = enemy
    else:
        action_first = versus(enemy, avatar)
        first_attack = enemy
        action_second = versus(avatar, enemy)
        second_attack = avatar

    return f"This time {first_attack.name} attacks first, and {action_first}" \
           f"\nNow {second_attack.name} attacks, and {action_second}"

