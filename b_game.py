import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 70, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Card class
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.face_up = True

    def draw(self, x, y):
        if self.face_up:
            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(screen, WHITE, card_rect)
            font = pygame.font.Font(None, 36)
            text = font.render(str(self.value), True, BLACK)
            screen.blit(text, (x + 5, y + 5))
        else:
            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(screen, BLACK, card_rect)

# Deck class
class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']:
            for value in range(1, 14):
                self.cards.append(Card(value, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

# Player class
class Player:
    def __init__(self):
        self.hand = []
        self.score = 0

    def draw(self, deck):
        card = deck.draw_card()
        self.hand.append(card)
        self.score += card.value

    def show_hand(self):
        for i, card in enumerate(self.hand):
            card.draw(100 + i * (CARD_WIDTH + 10), SCREEN_HEIGHT - CARD_HEIGHT - 10)

# Main Game Loop
def game_loop():
    deck = Deck()
    deck.shuffle()

    player = Player()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.draw(deck)

        # Clear screen
        screen.fill(GREEN)

        # Draw player's hand
        player.show_hand()

        # Update display
        pygame.display.flip()

game_loop()
pygame.quit()
