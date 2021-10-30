import random
import numpy as np
import time

def restore():
    global suit, face, foul_lst, bonus
    bonus = 0
    foul_lst = []
    face = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suit = ["♠", "♥", "♣", "♦"]

    player_setting()

def player_setting():  # Restore in Each NEW Game
    global name_lst, name_chip
    name_chip = {}
    running = True
    while running:
        try:
            num = int(input(f"enter number of player (min:2, max:9):    "))
            if num > 1 and num < 10:
                name_lst = [input(f"Player {i}, enter your name:   ") for i in range(num)]
                running = False
            print(f"Followings players:{name_lst}. Game is starting soon\n\n")

        except:
            print("Sorry, please try again!")

    for player in name_lst:
        name_chip[player] = 500
    new_round()

def add_(item, amount):
    item += amount
    return item

def new_round():
    global remain_lst, bonus, name_pt, name_card, deck
    deck = [(s + " " + f) for s in suit for f in face]
    random.shuffle(deck)
    name_pt = {}
    name_card = {}
    print("New round acquires 50 chips")
    remain_lst = [player for player in name_lst if player not in foul_lst]
    for player in remain_lst:
        if name_chip[player] <= 50:
            print(f" Sorry, {player} is fouled")
            foul_lst.append(player)
            continue
        if name_chip[player] > 50:
            print(f"{player} pays 50 chips to join the game")
            name_chip[player] -= 50
            bonus += 50

    for i in range(2):
        print("\nDealer is now distributing cards")
        for player in remain_lst:
            if player not in foul_lst:
                drawing(player, name_card)
            print(f"{player}: {name_card[player]}, {name_pt[player]}")
            
    hit_and_stand(foul_lst, name_lst, name_card, name_chip)

def drawing(player, name_card):  # Before hit and stand
    global card
    if player not in foul_lst:
        card = deck.pop()
        if player not in name_card:
            name_card[player] = card
        elif player in name_card:
            name_card[player] += ",  " + card
        point(player, name_pt, card)

def point(player, name_pt, card):
    if player not in name_pt:
        name_pt[player] = 0
    value = card.split(' ')[-1]
    if value.isdigit():
        pt = int(value)
    else:
        if value == "A":
            pt = 11
        else:
            pt = 10
    name_pt[player] += pt

def hit_and_stand(foul_lst, name_lst, name_card, name_chip):
    global stand_lst, bonus
    stand_lst = []
    give_up_lst = []
    remain_lst = [player for player in name_lst if player not in foul_lst]
    print(remain_lst)
    while len(give_up_lst) < len(remain_lst):
        print("\n")
        for player in remain_lst:
            if player not in stand_lst:
                ask = input(f"{player}, would you like to stand or hit?  Current pts: {name_pt[player]}   ").lower()
                if ask == "hit" or ask == "h":
                    drawing(player, name_card)
                    print(f"{player} hits, get{card}")

                elif ask == "stand" or ask == "s":
                    print(f"{player} stands")
                    stand_lst.append(player)

            elif player not in give_up_lst:
                bet = input(f"{player}, would you like to bet or not-bet or surrender?  Current pts: {name_pt[player]}   ").lower()
                if bet == "surrender" or bet == "surrend":
                    print(f"{player} surrender")
                    give_up_lst.append(player)

                elif bet == "bet" or bet == "b":
                    opt = input(f"{player}, would you like to free-bet or all-in?  "
                                f"Current pts: {name_pt[player]}, chips: {name_chip[player]}   ").lower()
                    if opt == "free-bet":
                        amt = int(input(f"{player}, how many chips you want to bet?   You now have: {name_chip[player]} chips   "))
                        if amt > name_chip[player]:
                            print(f"{player}, are you kidding me? You are skipped in this round")

                        elif name_chip == 0:
                            print(f"{player}, sorry to say that you will be fouled in next round as you have 0 chips")
                            give_up_lst.append(player)

                        else:
                            print(f"{player} bet {amt} chips")
                            bonus += amt
                            name_chip[player] -= amt

                    elif opt == "all-in":
                        if name_chip == 0:
                            print(f"{player}, sorry to say that you will be fouled in next round as you have 0 chips")

                        else:
                            print(f"{player} all-in {name_chip[player]}")
                            bonus += name_chip[player]
                            name_chip[player] -= name_chip[player]
                            give_up_lst.append(player)

                elif bet == "not-bet" or bet == "n":
                    print(f"{player} decides not to bet")
                    give_up_lst.append(player)

    round_winner()

def round_winner():
    bust_lst = []
    largest = []
    winner = []
    print("Dealer: Now player, open your cards\nChecking ...")
    for k, v in name_pt.items():
        if v > 21:
            bust_lst.append(k)
            continue
        largest.append(v)
    print(largest)
    large = max(largest)
    print("\n\n")
    for player in remain_lst:
        if name_pt[player] == large:
            winner.append(player)

    if bust_lst:
        print(f"Unfortunately, folowing player(s) bust: {bust_lst}. \nWinner(s) is(are) {winner}, Congratulations!!")

    else:
        print(f"Luckily, no player bust in this time. \nWinner(s) is(are) {winner}, Congratulations!!")
    fouling_loser(foul_lst, name_chip)
    final_winner(bonus, winner)

def fouling_loser(foul_lst, name_chip):
    for player in remain_lst:
        if name_chip[player] <= 0:  # fouling a player with 0 chip
            print(f"{player}, is fouled")
            foul_lst.append(player)

def final_winner(bonus, winner):
    lst_ = []
    win_num = len(winner)
    print(f"===================== {bonus} ==================")
    chips_num = np.arange(1, bonus+1)

    for i in chips_num:
        if i%win_num == 0:
            lst_.append(i)
    maxx_ = max(lst_)
    print(f"{winner} will receive {maxx_/win_num} chips")
    bonus -= maxx_

    for player in winner:
        name_chip[player] += maxx_/win_num

    if len(foul_lst) == len(name_lst) -1:
        for player in name_lst:
            if player not in foul_lst:
                print(f"The final winner is {player}, who owns {name_chip[player]} ships")
        next_game()

    else:
        print("Neext Round will be started on 5 seconds later\n\n")
        time.sleep(5)
        new_round()

def next_game():
    while True:
        ask = input("would you like to start a New Game?").lower()
        if ask == "yes":
            restore()
        elif ask == "no":
            print("See You")
            quit()
        else:
            print("Sorry, I don't understand. Please try again")

def main():
    restore()

main()
