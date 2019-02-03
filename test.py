from behaviour import *
import time

morale = 5
me_x = 1
player_x = 5
food_x = 3

def panicked():
    print("Checking Morale..")
    return morale <= 4

def flee():
    print("Monster fleeing")

def move_to_player():
    print("Moving toward player")
    global me_x, player_x
    if me_x <= player_x:
        me_x += 1

def can_see_player():
    x = (player_x - me_x <= 6)
    if x:
        print("I can see player")
        return True
    else:
        return False

def beside_player():
    x = (player_x - me_x <= 1)
    if x:
        print("I am beside player")
        return True
    else:
        return False

def attack_player():
    global morale
    print("attack player!")
    morale -= 1

def is_hungry():
    print("is hungry")

def food_in_range():
    print("food in range")
    return food_x - me_x <= 1

def move_to_food():
    print("moving towards food.")
    global me_x, food_x
    if me_x <=food_x:
        me_x += 1

def search_for_food():
    print("searching for food.")

def eat_food():
    print("eating food")

def wander():
    print("wandering idly")


ai = Tree(root=Selector(
    If(panicked, Action(flee)),
    If(beside_player, Action(attack_player)),
    If(can_see_player, Action(move_to_player)),
    If(is_hungry,
       If(food_in_range,
          Sequence(
              move_to_food,
              eat_food
          )
          ),
       search_for_food
       ),
    Action(wander)
))



for i in range(5):
    time.sleep(1)
    ai.tick()