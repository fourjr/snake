__import__('os').environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

from models import Apple, Colors, Snake


def draw_grid():
    for x in range(0, 800, 50):
        pygame.draw.line(screen, Colors.WHITE, (x, 0), (x, 800))

    for y in range(0, 800, 50):
        pygame.draw.line(screen, Colors.WHITE, (0, y), (800, y))


pygame.init()
pygame.display.set_caption('snake')
icon = pygame.image.load('snake.png')

pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800, 800))
screen.fill(Colors.GREY)
game_area = pygame.Rect((0, 0, 800, 800))

score = 0
font = pygame.font.Font('arial.ttf', 32)
text = font.render(str(score), True, Colors.WHITE)
textrect = text.get_rect()
textrect.right = 780
screen.blit(text, textrect)


draw_grid()
snake = Snake(screen)
apple = Apple(screen, snake)


eat_apple = pygame.USEREVENT + 1
game_over = False


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_w:
                    snake.turn('-y')
                if event.key == pygame.K_a:
                    snake.turn('-x')
                if event.key == pygame.K_s:
                    snake.turn('+y')
                if event.key == pygame.K_d:
                    snake.turn('+x')
            else:
                if event.key == pygame.K_SPACE:
                    screen.fill(Colors.GREY)
                    draw_grid()
                    snake = Snake(screen)
                    apple.regenerate()
                    game_over = False
                    score = 0
                    # restart game

        if event.type == snake.MOVE_EVENT and not game_over:
            old_screen = pygame.image.tostring(screen, 'RGB')
            screen.fill(Colors.GREY)
            draw_grid()
            snake.move()
            if not snake.inside(game_area) or snake.is_self_collide():
                # game over
                screen.blit(pygame.image.fromstring(old_screen, (800, 800), 'RGB'), (0, 0))
                arial_bold_font = pygame.font.Font('arial_bold.ttf', 64)
                text = arial_bold_font.render('Game Over', True, Colors.DARKER_RED)
                rect = text.get_rect()
                rect.center = (400, 375)
                screen.blit(text, rect)
                text = font.render('Press [space] to restart', True, Colors.WHITE)
                rect = text.get_rect()
                rect.center = (400, 425)
                screen.blit(text, rect)
                game_over = True
                continue
            else:
                if snake.colliderect(apple):
                    # apple eaten
                    snake.grow()
                    apple.regenerate()
                    score += 1
                else:
                    # draw apple since apple not eaten yet
                    pygame.draw.rect(screen, Colors.RED, apple.rect)

                snake.draw()
                text = font.render(str(score), True, Colors.WHITE)
                screen.blit(text, textrect)

        pygame.display.update()
