import pygame, random

#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Define Classes
class Game():
    """A class to help control and update gameplay"""

    def __init__(self, player, alien_group, player_bullet_group, alien_bullet_group):
        """Initialize the game"""
        #Set game values

        self.round_number = 1
        self.score = 0

        self.player = player
        self.alien_group = alien_group
        self.player_bullet_group = player_bullet_group
        self.alien_bullet_group = alien_bullet_group
        #Set sounds and music

        self.new_round_sound = pygame.mixer.Sound("new_round.wav")
        self.breach_sound = pygame.mixer.Sound("breach.wav")
        self.alien_hit_sound = pygame.mixer.Sound("alien_hit.wav")
        self.player_hit_sound = pygame.mixer.Sound("player_hit.wav")
        #Set font
        self.font = pygame.font.Font("Facon.ttf", 32)
    def update(self):
        """Update the game"""
        self.shift_aliens()
        self.check_collisions()
        self.check_round_completion()
    def draw(self):
        """Draw the HUD and other information to display"""
        pass

    def shift_aliens(self):
        """Shift a wave of aliens down the screen and reverse direction"""
        pass

    def check_collisions(self):
        """Check for collisions"""
        pass

    def check_round_completion(self):
        """Check to see if a player has completed a single round"""
        pass

    def start_new_round(self):
        """Start a new round"""
        # Create a grid of Aliens 11 columns and 5 rows.

        for col in range(11):
            for row in range(5):
                Alien(64 + col * 64, 64 + row * 64, self.round_number, self.alien_bullet_group)
                # first arg (x) is going to be 64 + col * 64
                # second arg (y) is going to be 64 + row * 64
                # third arg (velocity) is going to be self.round_number
                # fourth arg is self.alien_bullet_group
                self.alien_bullet_group.add(Alien)
        # Pause the game and prompt user to start
        # first arg (main_text) f"Space Invaders Round {self.round_number}"
        # second arg (sub_text) "Press 'Enter' to being"
        self.new_round_sound.play()
        self.pause_game(f"Space Invaders Round {self.round_number}", "Press 'Enter' to begin")
    def check_game_status(self, main_text, sub_text):
        """Check to see the status of the game and how the player died"""
        pass

    def pause_game(self, main_text, sub_text):
        """Pauses the game"""
        global running

        # Set Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        # Create main pause text
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        #Create sub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)
        #Blit the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()
        #Pause the game until the user hits enter
        #TODO: assign True to is_paused
        #TODO: while is_paused:
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
            #TODO: for event in pygame.event.get():
                # The user wants to play again
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                # The user wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False



    def reset_game(self):
        """Reset the game"""
        self.pause_game(f"Final Score: {self.score}", "Press 'Enter' to play again")
        # Reset game values

        self.score = 0
        self.round_number = 1
        self.player.lives = 5
        # Empty groups
        self.alien_group.empty()
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        # Start a new game
        self.start_new_round()


class Player(pygame.sprite.Sprite):
    """A class to model a spaceship the user can control"""

    def __init__(self, bullet_group):
        """Initialize the player"""
        super().__init__()

        self.image = pygame.image.load("player_ship.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.velocity = 8
        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound("player_fire.wav")

    def update(self):
        """Update the player"""

        keys = pygame.key.get_pressed()

        #Move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

    def fire(self):
        """Fire a bullet"""
        # Restrict the number of bullets on screen at a time=
        if len(self.bullet_group) < 2:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def reset(self):
        """Reset the player's position"""
        self.rect.centerx = WINDOW_WIDTH // 2

class Alien(pygame.sprite.Sprite):
    """A class to model an enemy alien"""

    def __init__(self, x, y, velocity, bullet_group):
        """Initialize the alien"""
        super().__init__()

        self.image = pygame.image.load("alien.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.starting_x = x
        self.starting_y = y

        self.direction = 1
        self.velocity = velocity
        self.bullet_group = bullet_group

        self.shoot_sound = pygame.mixer.Sound("alien_fire.wav")

    def update(self):
        """Update the alien"""
        self.rect.x += self.direction * self.velocity

        #Randomly fire a bullet
        if random.randint(0, 1000) > 999 and len(self.bullet_group) < 3:
            self.shoot_sound.play()
            self.fire()

    def fire(self):
        """Fire a bullet"""
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        """Reset the alien position"""
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1

class PlayerBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the player"""

    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()

        self.image = pygame.image.load("green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet"""
        self.rect.y -= self.velocity

        #If the bullet is off the screen, kill it
        if self.rect.bottom < 0:
            self.kill()

class AlienBullet(pygame.sprite.Sprite):
    """A class to model a bullet fired by the alien"""

    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()

        self.image = pygame.image.load("red_laser.png")
        self.image = self.image.set.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet"""
        self.rect.y += self.velocity

        #If the bullet is off the screen, kill it
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


#Create bullet groups
my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()

#Create a player group and Player object
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)

#Create an alien group.  Will add Alien objects via the game's start new round method
my_alien_group = pygame.sprite.Group()


#Create a Game object
my_game = Game(my_player, my_alien_group, my_player_bullet_group, my_alien_bullet_group)
my_game.start_new_round()

#The main game loop
running = True
while running:
    for event in pygame.event.get():

        # Check to see if the user wants to quit
        if event.type == pygame.QUIT:
            running = False

        #The player wants to fire
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                my_player.fire()

    #Fill the display
    display_surface.fill((0, 0, 0))

    #Update and display all sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_alien_group.update()
    my_alien_group.draw(display_surface)

    my_player_bullet_group.update()
    my_player_bullet_group.draw(display_surface)

    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(display_surface)



    #Update and draw a Game object
    pygame.display.update()

    #Update the display and tick the clock
    clock.tick(FPS)

#End the game
pygame.quit()