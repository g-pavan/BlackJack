import pygame
import random

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
FPS = 30

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Black Jack")

# Load card images or use solid colors if you don't have images
# Card image names should be like 'card_1.png', 'card_2.png', ... , 'card_10.png'
try:
    card_images = [pygame.image.load(f'card_{i}.png') for i in range(1, 11)]
except:
    card_images = [pygame.Surface((CARD_WIDTH, CARD_HEIGHT)) for _ in range(10)]
    for img in card_images:
        img.fill(WHITE)

# Simple card class
class Card:
    def __init__(self, value, image):
        self.value = value
        self.image = image

# Initialize deck
deck = [Card(value, image) for value, image in zip(range(1, 11), card_images) for _ in range(4)]

# Shuffle the deck
random.shuffle(deck)

# Draw text function
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Main loop
def game_loop():
    clock = pygame.time.Clock()
    player_hand = [deck.pop() for _ in range(2)]
    dealer_hand = [deck.pop() for _ in range(2)]

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Game logic here
        player_score = sum(card.value for card in player_hand)
        dealer_score = sum(card.value for card in dealer_hand)

        # Check for winner
        if player_score > 21:
            winner = "Dealer"
            game_over = True
        elif dealer_score > 21 or player_score == 21 or (dealer_score < player_score and len(player_hand) == 5):
            winner = "Player"
            game_over = True

        # Drawing
        screen.fill(GREEN)
        for i, card in enumerate(player_hand):
            screen.blit(card.image, (i * (CARD_WIDTH + 10), SCREEN_HEIGHT - CARD_HEIGHT - 10))
        for i, card in enumerate(dealer_hand):
            screen.blit(card.image, (i * (CARD_WIDTH + 10), 10))

        draw_text(f"Player Score: {player_score}", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        draw_text(f"Dealer Score: {dealer_score}", 24, WHITE, SCREEN_WIDTH // 2, 20)

        if game_over:
            draw_text(f"{winner} wins!", 40, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        pygame.display.flip()
        clock.tick(FPS)

# Run the game loop
game_loop()
pygame.quit()
