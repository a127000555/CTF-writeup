#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import os
from rng import RNG
from arts import maze, mazeDir, bossBG, gameOver, boom, win


# Constants
MAXDEPTH = 5
STAGE1SCORE = 5
MAXHP = 5
MAXBOSSHP = 50
DEBUG = 'DEBUG' in os.environ

if 'DVORAK' in os.environ:
    commands = ",oae.u'"  # Mapping from char to action ID
else:
    commands = "wsadefq"  # Mapping from char to action ID

# Offset of each direction
# Dir:      ^   v   <   >
moveOff = [-16, 16, -1, 1]


# Variable initialization
p = 198543992929796982831856294122484542605661595500963697094465382211596515703899
rng = RNG(p, pow(0xdeadbeef, 31337, p) // 2)
maze = [list(line) for line in maze.split('\n')]
player, monster = rng.extract(8), rng.extract(8)
items = {i: 0 for i in range(256)}
HP, BossHP, score = MAXHP, MAXBOSSHP, 0
history = ""  # For debug env


def draw(pos, c):
    """Draw a character on the dungeons map"""
    x, y = pos % 16 * 4 + 2, pos // 16 * 2 + 1
    maze[y][x] = c


def renderNormal():
    """Render normal stage"""
    # Draw moveable objects
    draw(monster, 'X')
    if monster == player:
        draw(player, 'B')
    elif items[player]:
        draw(player, 'G')
    else:
        draw(player, 'O')

    # Rendering
    print("Score                   Dungeons v2.0.0                        HP")
    print(("{:>05d}{:>60s}").format(score, 'x' * HP))
    print('\n'.join(''.join(line) for line in maze))

    # Remove moveable objects
    draw(player, 'i' if items[player] else ' ')
    draw(monster, 'i' if items[monster] else ' ')


def renderBoss():
    """Render boss stage"""
    # Draw boss HP bar
    print(' ' * 20, end='')
    print(('Boss |{:<%ds}| {:d}' % MAXBOSSHP).format('\u2588' * BossHP, BossHP))
    # Draw background
    print(bossBG)
    # Draw player HP bar
    print((' You |{:<%ds}| {:d}' % MAXHP).format('\u2588' * HP, HP))


def getAction():
    """Read from stdin and convert to action ID

    Action ID:
        id  key normal  boss
        0 - w - Up    / x
        1 - s - Down  / Surrender
        2 - a - Left  / Attack
        3 - d - Right / Defense
        4 - e - Pick  / x
        5 - f - Fight / Flee
        6 - q - Quit  / Quit

    -1 means unknown input
    """
    print("ent:",bin(rng.entropy_pool)[2:].rjust(256,'0'))
    print("m:",bin(rng.M)[2:].rjust(256,'0'))
    print(rng.entropy_pool)
    act = input('[>] action: ').lower()
    if DEBUG:
        global history
        history += act
        print(history)
    act = commands.find(act) if act else -1
    # act + 1 -> [0, 7] -> 3 bits entropy
    rng.entropy_from_keyboard(act + 1, 3)
    return act


def findPath(pos, depth, last):
    """Find the path to player shorter than MAXDEPTH step"""
    if depth == MAXDEPTH:
        return -1
    if player == pos:
        return pos

    for dir in range(4):
        # Never go back
        # Xor 1 will flip the direction
        if (last ^ 1) == dir:
            continue
        # Check the wall
        if mazeDir[pos][dir]:
            newPos = pos + moveOff[dir]
            if findPath(newPos, depth + 1, dir) != -1:
                return newPos
    return -1


def moveMonster():
    """Move the monster toward player

    Move the monster toward player if the distance to player is shorter
    than MAXDEPTH step, otherwise stay.
    """
    global monster
    newPos = findPath(monster, 0, 42)
    if newPos >= 0:
        monster = newPos


def monsterAttack():
    """Attack player if overlapped"""
    global HP
    if player == monster:
        HP -= rng.extract(2) + 1
        if HP <= 0:
            gameOver()
            if DEBUG:
                HP = 0
                return
            exit(0);


def normalStage():
    """Run normal stage

    Change to boss stage if the score is higher than STAGE1SCORE
    """
    global player, monster, HP, score
        
    while True:
        renderNormal()

        # Check win/lose condition
        if score > STAGE1SCORE:
            bossStage()

        # Player's round
        d = getAction()
        if d < 0:     # Stay
            pass
        elif d < 4:   # Move
            monsterAttack()  # Special case: run away
            # Check the wall
            if not DEBUG and not mazeDir[player][d]:
                boom()
            player += moveOff[d]
        elif d == 4:  # Pick
            assert(items[player])
            # Life regen
            items[player] -= 1
            draw(player, ' ')
            HP = min(MAXHP, HP + 1)
        elif d == 5:  # Attack
            assert(player == monster)
            score += 1
            items[monster] += 1
            # Spawn new monster
            while player == monster:
                monster = rng.extract(8)
            # Skip monster's round
            continue
        elif d == 6:  # Quit
            exit(0)

        # Monster's round
        monsterAttack()
        moveMonster()

        if DEBUG:
            print(rng.entropy_pool)


def bossStage():
    """Run boss stage

    Kill the super strong dragon to get the treasure
    """
    global HP, BossHP

    while True:
        renderBoss()

        # Check win/lose condition
        if HP == 0:
            gameOver()
            if not DEBUG:
                exit(0)
        if BossHP == 0:
            with open('../private/flag.txt') as f:
                win(f.read().strip())


        # Battling - Player
        a, defense = getAction(), 0
        if a == 2:    # Attack
            BossHP -= 1
        elif a == 1:  # Surrender
            HP = 0
        elif a == 3:  # Defense
            defense = 1
        elif a == 5:  # Flee
            print('[*] Failed')


        # Battling - Boss
        b = rng.extract(2)
        if b == 0:
            print('[*] Zzzzzzzzzzzz.')
        elif b == 1:
            print('[*] Hit.')
            HP -= 2 - defense
        elif b == 2:
            print('[*] A critical hit!')
            HP -= 5 + defense
        elif b == 3:
            print('[*] Life regen.')
            BossHP *= 2

        # Clipping values
        HP = max(0, min(MAXHP, HP))
        BossHP = max(0, min(MAXBOSSHP, BossHP))


if __name__ == '__main__':
    normalStage()
