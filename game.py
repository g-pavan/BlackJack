import pygame
import random

# Initialize Pygame
pygame.init()

# Global Variables
screen_width = 800
screen_height = 600
game_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Simple Blackjack')
font = pygame.font.SysFont(None, 55)
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

# Deck of Cards
cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*4

# Functions
def text_objects(text, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_to_screen(msg, color, x, y):
    text_surf, text_rect = text_objects(msg, color)
    text_rect.center = (x, y)
    game_screen.blit(text_surf, text_rect)

def game_loop():
    game_exit = False
    dealer_hand = []
    player_hand = []
    
    # Initial dealing for dealer and player
    for i in range(2):
        random.shuffle(cards)
        dealer_hand.append(cards.pop())
        player_hand.append(cards.pop())

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    player_hand.append(cards.pop())
                if event.key == pygame.K_s:
                    while sum(dealer_hand) < 17:
                        dealer_hand.append(cards.pop())
                    game_exit = True
        
        game_screen.fill(green)
        
        # Player Hand
        message_to_screen("Player Hand: " + str(player_hand) + " = " + str(sum(player_hand)), black, 400, 300)
        
        # Dealer Hand
        if game_exit:
            message_to_screen("Dealer Hand: " + str(dealer_hand) + " = " + str(sum(dealer_hand)), black, 400, 350)
        else:
            message_to_screen("Dealer Hand: [X, " + str(dealer_hand[1]) + "]", black, 400, 350)
        
        pygame.display.update()

        if sum(player_hand) > 21:
            message_to_screen('Player Busted!', red, 400, 400)
            pygame.display.update()
            pygame.time.wait(2000)
            game_exit = True
        
        if game_exit:
            if sum(dealer_hand) > 21 or sum(player_hand) > sum(dealer_hand):
                message_to_screen('Player Wins!', green, 400, 400)
            elif sum(player_hand) < sum(dealer_hand):
                message_to_screen('Dealer Wins!', red, 400, 400)
            else:
                message_to_screen('Push! Tie Game!', black, 400, 400)
            pygame.display.update()
            pygame.time.wait(2000)

        clock.tick(15)

game_loop()
pygame.quit()
quit()
