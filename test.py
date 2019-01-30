from behaviour import *
from random import randint

morale = 3
me_x = 0
player_x = 5
food_x = 3

def panicked():
    print("Morale check")
    return morale <= 4

def flee():
    print("Me flee!")

def move_to_player():
    print("move toward player")
    global me_x, player_x
    if me_x <=player_x:
        me_x += 1

def player_in_range():
    print("player in range")
    return player_x - me_x <= 6

def attack_player():
    print("attack player!")

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
    If(player_in_range, Sequence(
        Action(move_to_player),
        Action(attack_player),
    )),
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

ai.tick()
print("tick update 2")
ai.tick()