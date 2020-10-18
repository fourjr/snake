import random

import pygame


class Colors:
    GREY = pygame.Color(71, 106, 111)
    WHITE = pygame.Color(0, 0, 0)
    SNAKE = [
        pygame.Color(91, 80, 122),
        pygame.Color(91, 97, 138),
        pygame.Color(185, 226, 140),
        pygame.Color(158, 173, 200),
        pygame.Color(216, 214, 79),
        pygame.Color(78, 205, 196),
        pygame.Color(48, 99, 142),
        pygame.Color(98, 108, 102),
        pygame.Color(155, 151, 178),
        pygame.Color(250, 207, 173)
    ]
    RED = pygame.Color(209, 73, 91)
    DARKER_RED = pygame.Color(214, 26, 26)


class Snake:
    MOVE_EVENT = pygame.USEREVENT

    def __init__(self, screen):
        self.screen = screen
        self.delay = 300  # 1 pixel per x ms
        pygame.time.set_timer(self.MOVE_EVENT, self.delay)
        self.rects = [SnakePixel(0, 0, 50, 50, direction='+x', index=0)]
        self.draw()

    @property
    def size(self):
        return len(self.rects)

    @property
    def lefts(self):
        for i in self.rects:
            yield i.left

    @property
    def tops(self):
        for i in self.rects:
            yield i.top

    def move(self):
        for n, i in enumerate(reversed(self.rects)):
            n = self.size - 1 - n
            if n != 0:  # first element
                if self.rects[n - 1].turn_at and self.rects[n - 1].turn_at[0][:2] == (i.left, i.top):
                    i.direction = self.rects[n - 1].turn_at[0][2]
                    if self.size > n + 1:
                        i.turn_at.append((i.left, i.top, i.direction))
                    del self.rects[n - 1].turn_at[0]
            i.move()

    def draw(self):
        for i in self.rects:
            pygame.draw.rect(self.screen, i.color, i)

    def turn(self, direction):
        self.rects[0].direction = direction
        if self.size > 1:
            self.rects[0].turn_at.append((self.rects[0].left, self.rects[0].top, self.rects[0].direction))

    def grow(self):
        if self.rects[-1].direction == '+x':
            self.rects.append(SnakePixel(self.rects[-1].left - 50, self.rects[-1].top, 50, 50, direction=self.rects[-1].direction, index=self.size))
        if self.rects[-1].direction == '-x':
            self.rects.append(SnakePixel(self.rects[-1].left + 50, self.rects[-1].top, 50, 50, direction=self.rects[-1].direction, index=self.size))
        if self.rects[-1].direction == '+y':
            self.rects.append(SnakePixel(self.rects[-1].left, self.rects[-1].top - 50, 50, 50, direction=self.rects[-1].direction, index=self.size))
        if self.rects[-1].direction == '-y':
            self.rects.append(SnakePixel(self.rects[-1].left, self.rects[-1].top + 50, 50, 50, direction=self.rects[-1].direction, index=self.size))

        # speed up slightly after every apple eaten
        self.delay *= 0.9
        self.delay = int(self.delay)
        self.delay = max(self.delay, 100)
        pygame.time.set_timer(self.MOVE_EVENT, self.delay)

    def colliderect(self, rect):
        for i in self.rects:
            if i.colliderect(rect):
                return True
        return False

    def inside(self, rect):
        for i in self.rects:
            if not rect.contains(i):
                return False
        return True

    def is_self_collide(self):
        for i in self.rects:
            for j in self.rects:
                if i.index != j.index and i.colliderect(j):
                    return True
        return False


class SnakePixel(pygame.Rect):
    def __init__(self, *args, **kwargs):
        self.index = kwargs.pop('index')
        self.direction = kwargs.pop('direction')
        self.color = random.choice(Colors.SNAKE)
        self.turn_at = []
        super().__init__(*args, **kwargs)

    def move(self):
        if self.direction == '+x':
            self.left += 50
        if self.direction == '-x':
            self.left -= 50
        if self.direction == '+y':
            self.top += 50
        if self.direction == '-y':
            self.top -= 50


class Apple:
    def __init__(self, screen, snake):
        self.screen = screen
        self.snake = snake
        self.rect = pygame.Rect(random.randint(0, (800 - 50) // 50) * 50, random.randint(0, (800 - 50) // 50) * 50, 50, 50)
        pygame.draw.rect(screen, Colors.RED, self.rect)

    def regenerate(self):
        self.rect.left = random.randint(0, (800 - 50) // 50) * 50
        self.rect.top = random.randint(0, (800 - 50) // 50) * 50
        while self.rect.left in self.snake.lefts or self.rect.top in self.snake.tops:
            self.rect.left = random.randint(0, (800 - 50) // 50) * 50
            self.rect.top = random.randint(0, (800 - 50) // 50) * 50
        pygame.draw.rect(self.screen, Colors.RED, self.rect)
