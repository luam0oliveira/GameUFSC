import sys
import pygame
import spritesheet
import random

# Settings
FPS = 60
WIDTH = 400
HEIGHT = 700
DIMENSIONS = (WIDTH, HEIGHT)
DISTANCE_BETWEEN_OBJECTS = 160

# Init pygame
pygame.init()
screen = pygame.display.set_mode(DIMENSIONS)
clock = pygame.time.Clock()

# Load SpriteSheet
ss = spritesheet.SpriteSheet("assets/sprits/sprits.png")

# Load sprites from bird
bird_sprites = [
    ss.image_at((3, 491, 17, 12), (0,0,0)),
    ss.image_at((31, 491, 17, 12)),
    ss.image_at((59, 491, 17, 12))
]

for i in range(len(bird_sprites)):
    bird_sprites[i] = pygame.transform.scale_by(bird_sprites[i], 2.5)
    bird_sprites[i].set_colorkey((0, 0, 0))

animation_bird = pygame.USEREVENT + 0
pygame.time.set_timer(animation_bird, 300)

# Get the Sprites of bird
bird_surf = bird_sprites[0]
bird_rect = bird_surf.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
index = 0

# Background
background_image = pygame.transform.scale(ss.image_at((0, 0, 143, 255)), DIMENSIONS)

# Ground
ground_surf = pygame.transform.scale(ss.image_at((292, 0, 67, 56)), (WIDTH + 150, 150))
ground_rect = ground_surf.get_rect(bottomleft=(0, HEIGHT))

# Gravity
gravity = 0;

# Velocity of objects
velocity = 2;

# Generate distance between the obstacles
def generate_positions_of_objects():
    bottom_position = random.randint(170, 500)
    top_position = bottom_position - DISTANCE_BETWEEN_OBJECTS
    return [bottom_position, top_position]

positions = generate_positions_of_objects()
print(positions)

# Obstacles
# Bottom
bottom_obstacle_surf = pygame.transform.scale_by(ss.image_at((84, 323, 26, 160)), 3.5)
bottom_obstacle_surf.set_colorkey((0,0,0))
bottom_obstacle_rect = bottom_obstacle_surf.get_rect(topleft=(WIDTH, positions[0]))

# Top
top_obstacle_surf = pygame.transform.scale_by(ss.image_at((56, 323, 26, 160)), 3.5)
top_obstacle_surf.set_colorkey((0,0,0))
top_obstacle_rect = top_obstacle_surf.get_rect(bottomleft=(WIDTH, positions[1]))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            sys.exit()
        
        # Animation of bird
        if event.type == animation_bird:
            index += 1
            bird_surf = bird_sprites[index % len(bird_sprites)]
        
        # Bird jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gravity = -13


    screen.blit(background_image,background_image.get_rect(topleft=(0,0)))
    screen.blit(bottom_obstacle_surf, bottom_obstacle_rect)
    screen.blit(top_obstacle_surf, top_obstacle_rect)
    screen.blit(ground_surf, ground_rect)
    
    # Obstacles move
    bottom_obstacle_rect.x -= velocity
    top_obstacle_rect.x -= velocity

    # Ground animation
    ground_rect.x -= 1
    if ground_rect.x <= -100:
        ground_rect.x = 0

    # Bird gravity
    gravity += 1
    
    bird_rect.bottom += gravity

    if bird_rect.collidelist([top_obstacle_rect, bottom_obstacle_rect]) == 1:
        print("Fail")

    if bird_rect.bottom >= ground_rect.top:
        bird_rect.bottom = ground_rect.top
    
    screen.blit(bird_surf, bird_rect)
    pygame.display.update()

    clock.tick(FPS)

