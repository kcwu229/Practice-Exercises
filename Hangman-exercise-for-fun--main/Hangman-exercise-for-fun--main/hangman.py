import data_hangman as data
import random

# Basic setting
def basic_settings():
    print(data.opening)
    ask = input("\nPress p to start the game\t\t").lower()

    global word_4_game, guess_list, count, pics 
    pics = ''
    count = 0
    word_4_game = random.choice(data.words).lower()
    guess_list = list('_' * len(word_4_game))
    print(f'\n\n{guess_list}, remaining word(s): {guess_list.count("_")}\t\t remaining chance(s): {len(data.hangman_pics) - count}')
    pics = data.hangman_pics[0]
    print(pics)

    print("To play this game, you need to all alphabet in lower case."
    "Everytime you get wrong guess, your chances is deducted, and the man is steeping to death." 
    "When you get the correct answer or the man died, the game finished.")


# When player make per guess on letter
def guess():
    global count, ans, pics
    print()
    guess = input('Please guess a word:\t\t')

    for i, letter in enumerate(word_4_game):
        if guess in word_4_game:
            if guess == letter:
                guess_list[i] = guess
            ans = True

        else:
            ans = False
    
    if ans == False:
        count += 1
        pics = data.hangman_pics[count]
        print(f"Wrong!\t\n\n{pics}")
        ans = None

    else:
        print(f'Correct\t\n\n{pics}')
        ans = None
        
    print(f'\n\n{guess_list}, remaining word(s): {guess_list.count("_")}\t\t remaining chance(s): {len(data.hangman_pics) - count}')

# Decide whether the player would win/ lose 
def judge():
    if count < len(data.hangman_pics) and guess_list == word_4_game:
        print('You win!')
    else:
        print('You lose!')
    print(f"\n{word_4_game}")

# starter
def main():
    basic_settings()
    while pics != data.hangman_pics[-1]:
        guess()
    judge()

# only start if this .py is run as function
if __name__ == "__main__":
    main()