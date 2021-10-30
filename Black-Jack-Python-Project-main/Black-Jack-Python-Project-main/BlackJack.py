import random
import time

print('''
========================================================================================================================

========================================================================================================================

-----------  ----            ------    ------------ ----    ----      --------     ------    ------------ ----    ---- 
***********  ****           ********   ************ ****   ****       ********    ********   ************ ****   ****  
----       - ----          ----------  ---          ----  ----          ---      ----------  ---          ----  ----   
***********  ****         ****    **** ***          *********           ***     ****    **** ***          *********    
-----------  ----         ------------ ---          ---------           ---     ------------ ---          ---------    
****       * ************ ************ ***          ****  ****     ***   **     ************ ***          ****  ****   
-----------  ------------ ----    ---- ------------ ----   ----    --------     ----    ---- ------------ ----   ----  
***********  ************ ****    **** ************ ****    ****   ********     ****    **** ************ ****    **** 


========================================================================================================================

========================================================================================================================
    ''')
user = input("\nHello, What's your name?    ")


def setting():
    global deck, name_lst, name_pt, name_card
    face = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suit = ["♠", "♥", "♣", "♦"]
    deck = [(s + " " + f) for s in suit for f in face]
    name_lst = ["🤴", "🤵", "👳", "💰", user]
    name_pt = {}
    name_card = {}


def draw(player):
    random.shuffle(deck)
    global card
    time.sleep(0.5)
    card = deck.pop()
    if player not in name_card:
        name_card[player] = card
    elif player in name_card:
        name_card[player] += ",  " + card
    point(player, card)


def point(player, card):
    time.sleep(0.5)
    if player not in name_pt:
        name_pt[player] = 0
    num = card.split(" ")[-1]
    if num.isdigit():
        pt = int(num)
    else:
        if num == "A":
            pt = 11
        else:
            pt = 10
    name_pt[player] += pt


def hit_stand():
    stand_dict = {}
    while len(stand_dict) < len(name_lst):
        print("\n\nHit or Stand?")
        for player in name_lst:
            time.sleep(0.5)
            if player == user:
                if player not in stand_dict:
                    print(f"""

        ------------------
        |           {name_card[player][-4:]} |
        |                |
        |                |
        |                |
        |                |
        |       {name_card[player][-4:-2]}       |
        |                |
        |                |
        |                |
        |                |
        |                |
        | {name_card[player][-4:]}           |
        ------------------
 
                    """)
                    ask = input(f" {player}, would you like to hit or stand?   (Current pts:{name_pt[player]})").lower()
                    if ask == "s" or ask == "stand":
                        print(f"{player} stands")
                        stand_dict[player] = "Stand"
                    elif ask == "h" or ask == "hit":
                        draw(player)
                        print(f"{player} hits, gets {card}")
                    else:
                        print(f"{player}, since you do not follow my instruction, movement of this round is skipped!")
            elif player != user:
                if player not in stand_dict:
                    if name_pt[player] < 15:
                        draw(player)
                        print(f"{player} hits, gets {card}")
                    else:
                        print(f"{player} stands")
                        stand_dict[player] = "Stand"


def choosing_winner():
    bust_lst = []
    largest = []
    winner = []
    print("Dealer: Now player, open your cards\nChecking ...")
    time.sleep(0.5)
    for k, v in name_pt.items():
        if v > 21:
            bust_lst.append(k)
            continue
        largest.append(v)
    large = max(largest)
    print("\n\n")
    for player in name_lst:
        if name_pt[player] == large:
            winner.append(player)
    if bust_lst:
        print(f"Unfortunately, folowing player(s) bust: {bust_lst}. \nWinner(s) is(are) {winner}, Congratulations!!")
    else:
        print(f"Luckily, no player bust in this time. \nWinner(s) is(are) {winner}, Congratulations!!")
    print(f"Result: {name_pt}")


def again():
    count = 0
    while count < 3:
        try:
            again = input("Start a new Round?").lower()

            if again == "yes" or again == 'y':
                main()

            elif again == "no" or again =='n':
                print("See U")
                break

        except:
            print("Sorry, I don't understand. Please try again")
            count += 1
            if count == 3:
                print("Dealer: you are fooling me! You are no longer to be allowed to get in this casino")
                quit()


def main():
    setting()
    print("\nDealer is now distributing cards")
    print("Player,      Card in hand,      Points")
    for player in name_lst:
        draw(player)
        print(f"{player},              {name_card[player]},            {name_pt[player]}")

    print("\nDealer is now distributing cards")
    print("Player,      Card in hand,      Points")
    for player in name_lst:
        if player == user:
            draw(player)
            print(f"{player},              {name_card[player]},         {name_pt[player]}")
        else:
            print(f"{player},              {name_card[player]} + ? ,       {name_pt[player]} + ?")
            draw(player)
    hit_stand()
    choosing_winner()
    again()


if __name__ == "__main__":
    main()
