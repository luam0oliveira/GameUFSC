from app import App


# ss = spritesheet.SpriteSheet("assets/sprits/sprits.png")












app = App()
app.run()

# fb = FlappyBird(0, obstacle_images, background_image, ground_surf, bird_sprites)



# # Init pygame
# pygame.init()
# screen = pygame.display.set_mode(DIMENSIONS)
# clock = pygame.time.Clock()
#

#

#
# for i in range(len(bird_sprites)):
#     bird_sprites[i] = pygame.transform.scale_by(bird_sprites[i], 2.5)
#     bird_sprites[i].set_colorkey((0, 0, 0))
#
# animation_bird = pygame.USEREVENT + 0
# pygame.time.set_timer(animation_bird, 50)
#
# # Get the Sprites of bird
# bird_surf = bird_sprites[0]
# bird_rect = bird_surf.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
# index = 0
#
# # Background
# background_image = pygame.transform.scale(ss.image_at((0, 0, 143, 255)), DIMENSIONS)
#
# # Ground
# ground_surf = pygame.transform.scale(ss.image_at((292, 0, 67, 56)), (WIDTH + 150, 150))
# ground_rect = ground_surf.get_rect(bottomleft=(0, HEIGHT))
#
# # Gravity
# gravity = 0
#
# # Velocity of objects
# velocity = 0
#
#
# # Generate distance between the obstacles
# def generate_positions_of_objects():
#     bottom_position = random.randint(170, 500)
#     top_position = bottom_position - DISTANCE_BETWEEN_OBJECTS
#     return [bottom_position, top_position]
#
#
# positions = generate_positions_of_objects()
#
# # Obstacles
# # Bottom
# bottom_obstacle_surf = pygame.transform.scale_by(ss.image_at((84, 323, 26, 160)), 3.5)
# bottom_obstacle_surf.set_colorkey((0, 0, 0))
#
# # Top
# top_obstacle_surf = pygame.transform.scale_by(ss.image_at((56, 323, 26, 160)), 3.5)
# top_obstacle_surf.set_colorkey((0, 0, 0))
#
# bb = Bird(int(WIDTH / 2) - 100, int(HEIGHT / 2), bird_sprites)
#
# # Generate the first objects
# def generate_first_objects():
#     bottom_obstacle_rect = bottom_obstacle_surf.get_rect(topleft=(WIDTH + 400, positions[0]))
#
#     top_obstacle_rect = top_obstacle_surf.get_rect(bottomleft=(WIDTH + 400, positions[1]))
#     return [bottom_obstacle_rect, top_obstacle_rect]
#
#
# # Generating a pair of obstacles automatically
# obstacle_list = [generate_first_objects()]
#
# generate_pair_obstacle = pygame.USEREVENT + 1
# pygame.time.set_timer(generate_pair_obstacle, 1000)
#
# # Game over display
# font = pygame.font.Font(FONTS["bold"], size=32)
# game_over_text = font.render("Game over", False, (0, 0, 0))
# game_over_text_rect = game_over_text.get_rect(center=(int(WIDTH / 2), HEIGHT + 100))
#
# play_again_surf_alpha = 0
# play_again_surf = pygame.transform.scale_by(ss.image_at((354, 118, 52, 29)), 2)
# play_again_surf.set_alpha(play_again_surf_alpha)
# play_again_surf.set_colorkey((0, 0, 0))
# play_again_rect = play_again_surf.get_rect(center=(int(WIDTH / 2), int(HEIGHT / 2)))
#
# # Points
# gamePoint = 0
#
# game_point_text = font.render(str(gamePoint), False, (0, 0, 0))
# game_point_rect = game_point_text.get_rect(center=(int(WIDTH / 2), 100))
#
#
# def render_points(font_obj, points):
#     return font_obj.render(str(points), False, (0, 0, 0))
#
#
# def move_obstacles(list_of_obstacles):
#     if list_of_obstacles:
#         for obstacle in list_of_obstacles:
#             obstacle[0].x -= velocity
#             obstacle[1].x -= velocity
#
#             screen.blit(bottom_obstacle_surf, obstacle[0])
#             screen.blit(top_obstacle_surf, obstacle[1])
#         global gamePoint
#         if int(WIDTH / 2) == list_of_obstacles[0][0].x or len(list_of_obstacles) > 1 and list_of_obstacles[1][0].x == int(WIDTH / 2):
#             gamePoint += 1
#         list_of_obstacles = [obstacle for obstacle in list_of_obstacles if obstacle[0].x > -100]
#
#         return list_of_obstacles
#
#     return []
#
#
# # Game is over
# gameIsOver = False
#
# # Game is active
# active = False
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             running = False
#             sys.exit()
#
#         # Animation of bird
#         if event.type == animation_bird:
#             if gameIsOver:
#                 index = 2
#             else:
#                 index += 1
#             bird_surf = bird_sprites[index % len(bird_sprites)]
#             bird_surf.set_colorkey((0, 0, 0))
#
#         # Bird jump
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE and not gameIsOver:
#                 if active:
#                     gravity = -13
#                     velocity = 2
#                 active = True
#
#         if event.type == generate_pair_obstacle and active:
#             positions = generate_positions_of_objects()
#
#             distance = obstacle_list[len(obstacle_list) - 1][0].x + DISTANCE_BETWEEN_PAIR_OBJECTS
#
#             bottom_obstacle_rect = bottom_obstacle_surf.get_rect(topleft=(distance, positions[0]))
#             top_obstacle_rect = top_obstacle_surf.get_rect(bottomleft=(distance, positions[1]))
#             obstacle_list.append([bottom_obstacle_rect, top_obstacle_rect])
#
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gameIsOver:
#             if play_again_rect.collidepoint(event.pos):
#                 obstacle_list = [generate_first_objects()]
#                 gravity = 0
#                 velocity = 0
#                 bird_rect.center = (int(WIDTH / 2), int(HEIGHT / 2))
#                 gameIsOver = False
#                 gamePoint = 0
#                 play_again_surf_alpha = 0
#                 play_again_surf.set_alpha(play_again_surf_alpha)
#                 game_over_text_rect.center = (int(WIDTH / 2), HEIGHT + 100)
#
#     screen.blit(background_image, background_image.get_rect(topleft=(0, 0)))
#     obstacle_list = move_obstacles(obstacle_list)
#     screen.blit(ground_surf, ground_rect)
#
#     # Bird rotation
#     bird_surf = pygame.transform.rotate(bird_sprites[index % len(bird_sprites)], -gravity)
#     bird_surf.set_colorkey((0, 0, 0))
#
#     # Ground animation
#     if not gameIsOver:
#         ground_rect.x -= velocity
#     if ground_rect.x <= -100:
#         ground_rect.x = 0
#
#     # Bird gravity and game over
#     if gameIsOver:
#         gravity = 10
#         velocity = 0
#     elif active:
#         gravity += 1
#
#     bird_rect.bottom += gravity
#
#     if bird_rect.collidelist(obstacle_list[0]) != -1 or (len(obstacle_list) >= 2
#                                                          and bird_rect.collidelist(obstacle_list[1]) != -1) or bird_rect.bottom >= HEIGHT - 150:
#         gameIsOver = True
#
#     if bird_rect.bottom >= ground_rect.top:
#         bird_rect.bottom = ground_rect.top
#
#     screen.blit(bird_surf, bird_rect)
#     game_point_text = render_points(font, gamePoint)
#     screen.blit(game_point_text, game_point_rect)
#
#     if gameIsOver:
#         if game_over_text_rect.y >= 400:
#             game_over_text_rect.y -= 5
#         else:
#             play_again_surf_alpha += 10
#             play_again_surf.set_alpha(play_again_surf_alpha)
#
#         pygame.draw.rect(screen, 'Blue', game_over_text_rect.inflate(10, 10), border_radius=10)
#         screen.blit(game_over_text, game_over_text_rect)
#         screen.blit(play_again_surf, play_again_rect)
#
#     bb.update()
#     screen.blit(bb.image, bb.rect)
#
#
#     pygame.display.update()
#
#     clock.tick(FPS)
