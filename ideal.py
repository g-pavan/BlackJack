import pygame
import sys
import random

class BlackJack:
    def __init__(self):
        # Initialize the deck with card values
        self.cards = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}
        # Initialize player and dealer hands with two random cards each
        self.player_hand = list(random.sample(list(self.cards.keys()), 2))
        self.dealer_hand = list(random.sample(list(self.cards.keys()), 2))
        # Calculate the initial sum of cards in each hand
        self.player_deck_sum = self.get_deck_sum(self.player_hand)
        self.dealer_deck_sum = self.get_deck_sum(self.dealer_hand)
    
    def check_blackJack(self, deck):
        # Check if a hand is a blackjack (contains '10' and 'A')
        if(len(deck) ==  2 and '10' in deck and 'A' in deck):
            return True
        return False

    def add_card_to_player(self):
        # Add a random card to the player's hand
        card = list(random.sample(list(self.cards.keys()), 1))[0]
        self.player_deck_sum += self.get_card_values(card)
        self.player_hand.append(card)
    
    def add_card_to_dealer(self):
        # Add a random card to the dealer's hand
        card = list(random.sample(list(self.cards.keys()), 1))[0]
        self.dealer_deck_sum += self.get_card_values(card)
        self.dealer_hand.append(card)

    def get_card_values(self,key):
        # Get the value of a card from the deck
        return self.cards.get(key, 0)
    
    def get_deck_sum(self, deck):
        # Calculate the sum of card values in a deck, accounting for Ace as 11 or 1
        sum = 0
        flag = False
        
        for key in deck:
            if(key == 'A'):
                flag = True
                sum += 11
            else:   
                sum += self.get_card_values(key)
            
        if(sum > 21 and flag):
            sum -= 10

        return sum

    def determine_winner(self):
        # Determine the winner based on the sum of card values in hands
        if self.player_deck_sum > 21:
            return "Bust! You lose."
        elif self.dealer_deck_sum > 21:
            return "You win!"
        elif self.player_deck_sum > self.dealer_deck_sum:
            return "You win!"
        elif self.player_deck_sum < self.dealer_deck_sum:
            return "You lose!"
        else:
            return "Push! Tie Game!"

# Game loop
class Game():
    def __init__(self):
        self.blackJack = None
        # Constants for screen setup
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 600
        self.CARD_WIDTH, self.CARD_HEIGHT = 70, 100
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)

        # Setup the screen
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Blackjack")

        # Define button properties for in-game and end game scenarios
        self.button_data = [
            {"rect": pygame.Rect(625, 350, 150, 75), "color": (34, 125, 247), "name": "Stand"},
            {"rect": pygame.Rect(25, 350, 150, 75), "color": (34, 125, 247), "name": "Hit"},
            {"rect": pygame.Rect(325, 450, 150, 75), "color": (255, 0, 0), "name": "Quit"},
        ]

        self.end_button_data = [
            {"rect": pygame.Rect(400, 450, 150, 75), "color": (125, 105, 175), "name": "Play Again!"},
            {"rect": pygame.Rect(200, 450, 150, 75), "color": (255, 0, 0), "name": "Quit"},
        ]

        # Setup fonts for button and result text
        self.font = pygame.font.Font(None, 36)  # Use the default font with size 36
        self.result_font = pygame.font.Font(None, 48)

        # Game status flags
        self.status = False
        self.text = ''
        self.end = False
    
    def new_game(self,):
        # Reset game state for a new game
        self.status = False
        self.text = ''
        self.end = False
        self.blackJack = BlackJack()
        pygame.display.update()

    def draw_hand(self, hand, x, y, hide_card=False):
        # Draw the cards in a hand on the screen
        for i, card_value in enumerate(hand):
            if i == 0 and hide_card:
                # Draw an "X" for the second card (hidden)
                pygame.draw.rect(self.screen, self.WHITE, (x + i * (self.CARD_WIDTH + 10), y, self.CARD_WIDTH, self.CARD_HEIGHT))
                x_text = self.font.render("X", True, self.BLACK)
                x_rect = x_text.get_rect(center=(x + i * (self.CARD_WIDTH + 10) + self.CARD_WIDTH // 2, y + self.CARD_HEIGHT // 2))
                self.screen.blit(x_text, x_rect)
            else:
                pygame.draw.rect(self.screen, self.WHITE, (x + i * (self.CARD_WIDTH + 10), y, self.CARD_WIDTH, self.CARD_HEIGHT))
                card_text = self.font.render(str(card_value), True, self.BLACK)
                card_rect = card_text.get_rect(center=(x + i * (self.CARD_WIDTH + 10) + self.CARD_WIDTH // 2, y + self.CARD_HEIGHT // 2))
                self.screen.blit(card_text, card_rect)
    
    def text_objects(self, text, color):
        # Create a text surface and rectangle for positioning
        text_surface = self.font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def message_to_screen(self, msg, color, x, y):
        # Display a message on the screen
        text_surf, text_rect = self.text_objects(msg, color)
        text_rect.center = (x, y)
        self.screen.blit(text_surf, text_rect)

    def handle_button_click(self, button_name):
        # Handle button clicks based on the button name
        if button_name == "Hit":
            self.blackJack.add_card_to_player()
            if(self.blackJack.player_deck_sum > 21 or self.blackJack.dealer_deck_sum > self.blackJack.player_deck_sum):
                self.status = True
                self.text = self.blackJack.determine_winner()
        elif button_name == "Stand":
            while(self.blackJack.dealer_deck_sum < 17):
                self.blackJack.add_card_to_dealer()
            self.status = True
            self.text = self.blackJack.determine_winner()
        elif button_name == "Quit":
            pygame.quit()
            sys.exit()
        elif button_name == "Play Again!":
            self.new_game()

    def start_game(self):
        # Main game loop
        self.new_game()

        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle button clicks based on mouse position
                    if(not self.end):
                        for button in self.button_data:
                            if button["rect"].collidepoint(event.pos):
                                self.handle_button_click(button["name"])
                    else:
                        for end_button in self.end_button_data:
                            if end_button["rect"].collidepoint(event.pos):
                                self.handle_button_click(end_button["name"])

            # Clear the screen
            self.screen.fill(self.GREEN)

            # Draw the buttons
            if(not self.end):
                for button in self.button_data:
                    pygame.draw.rect(self.screen, button["color"], button["rect"])
                    button_text = self.font.render(button["name"], True, (0, 0, 0))
                    text_rect = button_text.get_rect(center=button["rect"].center)
                    self.screen.blit(button_text, text_rect)
            else:
                for end_button in self.end_button_data:
                    pygame.draw.rect(self.screen, end_button["color"], end_button["rect"])
                    button_text = self.font.render(end_button["name"], True, (0, 0, 0))
                    text_rect = button_text.get_rect(center=end_button["rect"].center)
                    self.screen.blit(button_text, text_rect)
                
                self.message_to_screen(self.text , self.BLACK, 400, 400)

            # Draw player hand
            self.draw_hand(self.blackJack.player_hand, 475, 100)
            self.message_to_screen("Player Hand: " + ", ".join(self.blackJack.player_hand) + " = " + str(self.blackJack.player_deck_sum), self.BLACK, 600, 225)

            if self.status:
                # Show the dealer's hand and determine the winner
                self.draw_hand(self.blackJack.dealer_hand, 50, 100)
                self.message_to_screen("Dealer Hand: " + ", ".join(self.blackJack.dealer_hand) + " = " + str(self.blackJack.dealer_deck_sum), self.BLACK,  150, 225)
                self.message_to_screen(self.text , self.BLACK, 400, 400)
                pygame.display.update()
                pygame.time.wait(2000)
                self.end = True
            else:
                # Show the dealer's hand with the first card hidden
                self.draw_hand(self.blackJack.dealer_hand, 50, 100, True)
                self.message_to_screen("Dealer Hand: X, " + ", ".join(self.blackJack.dealer_hand[1:]) , self.BLACK, 125, 225)
            
            if self.blackJack.check_blackJack(self.blackJack.player_hand):
                # Check for player blackjack and handle the result
                if self.blackJack.check_blackJack(self.blackJack.dealer_hand):
                    self.text  = "It's BlackJack! Oops, Push with Dealer!"
                else:
                    self.text  = "It's BlackJack! You Won."
                self.message_to_screen(self.text , self.BLACK, 400, 300)
                pygame.display.flip()
                pygame.time.wait(2000)
                self.end = True

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(60)


if __name__ == "__main__":

    # Initialize Pygame
    pygame.init()

    game = Game()
    game.start_game()

    pygame.quit()
