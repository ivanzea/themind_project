import pygame
import pygame.freetype
import numpy as np

# Initialize pygame
pygame.init()
gamefont = pygame.freetype.SysFont('Calibri_bold', 30)

# Parameters


# Draw player hands
def draw_env(screen, card_sprites, hand_cards, public_card, level, lives, shurikens, visible=False):
    # Fixed drawing paramenters
    card_gap = (55, 40)  # pixels between cards in hand (x, y)

    # Screen elements dimensions
    xscreen = screen.get_size()[0]
    yscreen = screen.get_size()[1]
    card_size = card_sprites[0].get_size()

    # Get parameters from environment
    hand_cards = hand_cards
    public_card = public_card
    level = level
    shurikens = shurikens
    lives = lives

    # Draw player hands
    for ply, hand in enumerate(hand_cards):
        n_cards = len(hand)
        if (ply == 0):  # bottom position P1
            init_xpos = xscreen//2 - (card_size[0] + card_gap[0]*(n_cards-1))//2
            for ci, card in enumerate(hand):  # loop through the hand
                screen.blit(card_sprites[card-1], [init_xpos + card_gap[0]*(ci),  # x-coor
                                                   yscreen-card_size[1]])           # y-coor
        elif (ply == 1):  # top position P2
            init_xpos = xscreen//2 - (card_size[0] + card_gap[0]*(n_cards-1))//2
            for ci, card in enumerate(hand):  # loop through the hand
                card_disp = card_sprites[card-1] if visible else card_sprites[-1]
                screen.blit(card_disp, [init_xpos + card_gap[0]*(ci),            # x-coor
                                        0])                                        # y-coor
        elif (ply == 2):  # left position P3
            init_ypos = yscreen//2 - (card_size[1] + card_gap[1]*(n_cards-1))//2
            for ci, card in enumerate(hand):  # loop through the hand
                card_disp = card_sprites[card-1] if visible else card_sprites[-1]
                screen.blit(card_disp, [0,                                         # x-coor
                                        init_ypos + card_gap[1]*(ci)])           # y-coor
        elif (ply == 3):  # left position P4
            init_ypos = yscreen//2 - (card_size[1] + card_gap[1]*(n_cards-1))//2
            for ci, card in enumerate(hand):  # loop through the hand
                card_disp = card_sprites[card-1] if visible else card_sprites[-1]
                screen.blit(card_disp, [xscreen-card_size[0],                     # x-coor
                                        init_ypos + card_gap[1]*(ci)])          # y-coor

    # Draw public card
    screen.blit(card_sprites[public_card-1], [xscreen//2 - card_size[0]//2, yscreen//2 - card_size[1]//2])

    # Draw shurikens

    # Draw level
    level_text_loc = [xscreen - live_sprite.get_size()[0]*3, gamefont.size*1.3]
    level_text, _ = gamefont.render(f'LVL : {level}', (0, 0, 0))
    screen.blit(level_text, level_text_loc)

    # Draw lives
    heart_location = [xscreen - live_sprite.get_size()[0]*3, gamefont.size*2]
    screen.blit(live_sprite, heart_location)

    lives_text_loc = heart_location
    lives_text_loc[0] += live_sprite.get_size()[0]
    lives_text_loc[1] += lives_text_loc[1]/4
    lives_text, _ = gamefont.render(f' : {lives}', (0, 0, 0))
    screen.blit(lives_text, lives_text_loc)


# Initial screen
screen = pygame.display.set_mode((1200, 800))

# Change Title and icon
pygame.display.set_caption("The Mind")
icon = pygame.image.load("bin/images/themind.png")
pygame.display.set_icon(icon)

# Load card sprites
card_sprites = []
for card_number in range(100):
    card_sprites.append(pygame.image.load(f'bin/images/card-{card_number+1}.png'))
card_sprites.append(pygame.image.load("bin/images/card-back.png"))  # card back in position -1

live_sprite = pygame.image.load("bin/images/full_heart.png")

# Existing window loop
running = True
while running:
    # Background color
    screen.fill((53, 101, 77))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_env(screen, card_sprites, [[99, 55, 44, 2, 6, 34, 35, 36, 37, 38, 39, 42],
                                    [88, 66, 10, 77, 78, 79, 80, 81, 82, 83, 84, 85],
                                    [1, 3, 5, 8, 9, 12, 13, 14, 15, 100, 20, 30],
                                    [50, 51, 52]],
             99,
             12,
             2,
             3,
             False)

    pygame.display.update()
