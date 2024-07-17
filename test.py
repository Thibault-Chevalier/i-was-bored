import random
import matplotlib.pyplot as plt
from collections import Counter
import bisect

N_tests = 100000 # Number of simulations
drawn_cards_limit = 100 # Limit of cards drawn for resonable computation time
mill_treshold = 20 # Treshold for mill probability
max_cards_in_hand = 10 # Maximum number of cards in hand

def test(N):# N = number of Packages Dealers # Supposing PD activates when milling/fatigue
    total_cards_drawn = 1 # Start by drawing 1 card
    list_PD = [0] * N # list of PD activations
    cards_to_draw = 1 # Start by drawing 1 card
    while cards_to_draw > 0 and total_cards_drawn < drawn_cards_limit :
        for cards in range(cards_to_draw): # For each drawn card
            for i in range(N): # For each PD
                # 50% PD activations
                if random.random() > 0.5:
                    list_PD[i] += 1
            # print(f"PD activations for card drawn n°{total_cards_drawn} : {list_PD}")
        cards_to_draw = sum(list_PD)
        total_cards_drawn += cards_to_draw
        list_PD = [0] * N
    return min(drawn_cards_limit, total_cards_drawn)

def test2(nb_PD, cards_in_hand, cards_in_deck):# N = number of Packages Dealers # Supposing PD doesn't activates when milling/fatigue
    list_PD = [0] * nb_PD # list of PD activations
    total_cards_drawn = 1 # Start by drawing 1 card
    cards_to_draw = 1 # Start by drawing 1 card
    while cards_to_draw > 0 and total_cards_drawn < drawn_cards_limit :
        for cards in range(cards_to_draw): # For each drawn card
            if cards_in_hand < max_cards_in_hand and cards_in_deck > 0:
                cards_in_hand += 1
                cards_in_deck -= 1
                for i in range(nb_PD): # For each PD
                    # 50% PD activations
                    if random.random() > 0.5:
                        list_PD[i] += 1
                # print(f"PD activations for card drawn n°{total_cards_drawn} : {list_PD}")
        cards_to_draw = sum(list_PD)
        total_cards_drawn += cards_to_draw
        list_PD = [0] * nb_PD
    return min(drawn_cards_limit, total_cards_drawn)

def proba(list_results):
    N_tests = len(list_results)
    count_results = Counter(list_results)# Count occurrences of each number in the list
    label, count = zip(*sorted(list(count_results.items())),  strict=True)# Extract the numbers labels and their probabilities
    probabilities = [c / N_tests for c in count]
    return label, probabilities

def graph_test(label, probabilities, ):
    plt.plot(label, probabilities, '.', color='royalblue')

    ### Horyzontal lines for interesting theoretical probabilities
    # # Probability of activating at least 1 PD
    # P = 1-(1/2**N)
    # print("The probability at least 1 activating", P)
    # plt.hlines(y=P, xmin=1.5, xmax=drawn_cards_limit, color='red', linestyle='--', label='at least 1 activating')
    # plt.vlines(x=1.5, ymin=0, ymax=P, color='red', linestyle='--')
    # # Probability of activating at least 2 PD
    # if N > 1:
    #     P = 1-(N*1/2**N)
    #     print("The probability at least 2 activating", P)
    #     plt.hlines(y=P, xmin=2.5, xmax=drawn_cards_limit, color='orangered', linestyle='--', label='at least 2 activating')
    #     plt.vlines(x=2.5, ymin=0, ymax=P, color='orangered', linestyle='--')
    # Probability of drawing 30+ cards
    # mill_treshold_pos = bisect.bisect_left(label, mill_treshold)
    # proba_mill = sum(probabilities[mill_treshold_pos:])
    # print(f"The probability of drawing {mill_treshold}+ cards is {proba_mill}")
    # plt.hlines(y=proba_mill, xmin=mill_treshold, xmax=drawn_cards_limit, color='green', linestyle='--', label=f'{mill_treshold}+ cards')
    # plt.vlines(x=mill_treshold, ymin=0, ymax=proba_mill, color='green', linestyle='--')
    # mill_treshold_pos = bisect.bisect_left(label, mill_treshold)
    # proba_mill = sum(probabilities[mill_treshold_pos:])
    # print(f"The probability of drawing {mill_treshold}+ cards is {proba_mill}")
    # plt.vlines(x=mill_treshold, ymin=0, ymax=0.2, color='green', linestyle='--', label=f'{mill_treshold}+ cards')


if __name__=="__main__":
    starting_cards_in_hand = 0
    starting_cards_in_deck = 10
    hp = 30
    mill_treshold = int((2*hp+1/4)**0.5-1/2)+1+starting_cards_in_deck
    print(f"Mill treshold for {hp}hp with {starting_cards_in_deck} cards in deck is {mill_treshold} cards")

    for N in range (2, 8):
    # for N in range (2, 3):

        list_results = [test2(N, starting_cards_in_hand, starting_cards_in_deck) for i in range(N_tests)]
        nb_draws, probabilities = proba(list_results)

        # mill_treshold_pos = bisect.bisect_left(nb_draws, mill_treshold)
        # proba_mill = sum(probabilities[mill_treshold_pos:])
        # print(f"The probability of drawing {mill_treshold}+ cards is {proba_mill}")
        # plt.vlines(x=mill_treshold, ymin=0, ymax=0.2, color='green', linestyle='--', label=f'{mill_treshold}+ cards')

        # plt.plot(nb_draws, probabilities, '.', color = 'blue', label='Cards drawn')

        # plt.xlabel('Cards drawn')
        # plt.ylabel(f'Probability, N = {N_tests}')
        # plt.title(f'Probability Distribution for {N} Package Dealers,\n{starting_cards_in_hand} cards in hand, {starting_cards_in_deck} cards in deck')
        # plt.legend()

        # plt.show()

        nb_fatigue = [max(0,draws-starting_cards_in_deck) for draws in nb_draws] # Fatigue damage calculation
        damage_fatigue = [fatigue*(fatigue+1)/2 for fatigue in nb_fatigue] # Simple sum of arithmetic progression
        
        no_fatigue = [fatigue for fatigue in nb_fatigue if fatigue == 0] # element where 0 fatigue
        nb_supr = len(no_fatigue)-1 # number of repeated 0 fatigue
        nb_fatigue = nb_fatigue[nb_supr:] # remove 0 fatigue but one
        damage_fatigue = damage_fatigue[nb_supr:] # remove 0 fatigue but one
        fatigue_probabilities = probabilities[nb_supr:] # remove 0 fatigue but one
        fatigue_probabilities[0] += sum(probabilities[:nb_supr]) #recalculate the probability of 0 fatigue

        mill_treshold_pos = bisect.bisect_left(damage_fatigue, hp)
        proba_mill = sum(fatigue_probabilities[mill_treshold_pos:])
        print(f"The probability of dealing {hp}+ fatigue damage with {N} Package Dealers is {proba_mill}")
        plt.vlines(x=hp, ymin=0, ymax=0.2, color='green', linestyle='--', label=f'{hp}+ damage')

        plt.plot(damage_fatigue, fatigue_probabilities, '-o', color = 'red', label='Fatigue damage')
        
        plt.xlabel('Fatigue damage')
        plt.ylabel(f'Probability, N = {N_tests}')
        plt.title(f'Probability Distribution for {N} Package Dealers,\n{starting_cards_in_hand} cards in hand, {starting_cards_in_deck} cards in deck')
        plt.legend()
       
        plt.show()
