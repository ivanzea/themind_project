import gym
from gym import spaces

import random
import math


class Player():

    def __init__(self, hand):
        # Initialize variables
        self.hand = hand.copy()
        self.empty_hand = False

        self.hand.sort()  # ascending order
        self.card2play = self.hand[0]

    def play_card(self):
        card_played = []
        
        if not self.empty_hand:
            card_played = self.hand.pop(0)

            if not self.hand:
                self.card2play = []
                self.empty_hand = True
            else:
                self.card2play = self.hand[0]

        return card_played


class TheMind(gym.Env):

    def __init__(self, starting_level=1, players=2):
        # Initialize variables
        self.level = starting_level
        self.num_players = players

        self.lives = 3
        self.min_action = 0.01
        self.max_action = 90
        self.min_deck = 1
        self.max_deck = 100
        self.max_level = 12

        # Define action space
        self.action_space = spaces.Box(
            low=self.min_action,
            high=self.max_action,
            shape=(1,))

        # Initialize level
        self.init_level()

    def step(self, pid):
        done = False
        reward = 0
        
        # Check that a play can be done... hand is not empty
        if not self.players[pid].empty_hand:
            # Play card
            card_played = self.players[pid].play_card()

            # Was it an incorrect play?
            card_position = self.correct_order.index(card_played)
            if card_position != 0:
                self.played_card = card_played
                reward = -1
                self.lives -= card_position
                
                if self.lives == 0:
                    done = True
                    return reward, done
            else:
                self.played_card = card_played
                reward = 1

            # Remove played card from correct card order and 
            # any other cards incorrectly held in hand
            for card_rm in self.correct_order[:card_position]:
                for ply in self.players:
                    if ply.card2play == card_rm:
                        ply.play_card()
                        break
            self.correct_order = self.correct_order[card_position+1:]
            
            # Check if all the players hands are empty
            done = all([ply.empty_hand for ply in self.players])
            
        return reward, done

    def reset(self):
        if (self.lives < 1) | (self.level == self.max_level):
            self.level = 1
            self.lives = 3
        else:
            self.level += 1

        self.init_level()

    def render(self, result=0, show_all=False):
        """
        Text render of the game
        visible_player -> player hand to see if = 0, ALL hands are visible
        """
        print(f'lvl : {self.level}       lives: {self.lives}')
        print('-----------------------------------------')
        print(f'Last Card Played : {self.played_card}')
        print('')
        print('Hand Cards : ')
        for pid, p in enumerate(self.players):
            print('Player ', pid+1, ' -> ', end='')
            if (pid == 0) | (show_all):
                print(*p.hand, sep=', ')
            else:
                out = '[X], ' * len(p.hand)
                print(out[:-2])
        print('')
        

    def init_level(self):
        # Initialize variables
        self.deck = []
        self.players = []
        self.played_card = 0

        self.deck = random.sample(range(self.min_deck, self.max_deck+1),
                                  self.level*self.num_players)
        self.correct_order = sorted(self.deck)

        # Create players
        for _ in range(self.num_players):
            self.players.append(Player(hand=self.deck[:self.level]))
            # Remove delt cards from deck
            self.deck = self.deck[self.level:]
