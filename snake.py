import pygame, sys, random, numpy as np
from pygame import Vector2

pygame.init()

foregroundColour = (108, 255, 109)
backgroundColour = (124, 233, 255)
border_colour = (255, 102, 255)

cell_size = 30
number_of_cells = 25

class Food:
    def __init__(self, snake):
        self.snake = Snake()
        self.position = self.generate_random_pos(snake)

    def draw(self):
        foodRect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, foodRect)
    def generate_random_coord(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)
    def generate_random_pos(self, snake_coords):
        position = self.generate_random_coord()
        while position in snake_coords:
            position = self.generate_random_coord()
        return position

class Snake:
    def __init__(self):
        self.snake = [Vector2(4,4), Vector2(5,4), Vector2(6,4), Vector2(7,4)]
        self.head = [self.snake[-1]]
        self.body = [self.snake[1:-1]]
        self.tail = [self.snake[0]]
        self.direction = Vector2(1,0)
        self.oldSnakeYCoord = self.tail[0].y
        self.oldSnakeXCoord = self.tail[0].x
        self.add_segment = False

    def draw(self):
        headRect = (self.head[0].x * cell_size, self.head[0].y * cell_size, cell_size, cell_size)
        tailRect = (self.tail[0].x * cell_size, self.tail[0].y * cell_size, cell_size, cell_size)
        if self.snake[1].x > self.snake[0].x:
            screen.blit(tail_left_surface, tailRect)
        elif self.snake[1].y > self.snake[0].y:
            screen.blit(tail_up_surface, tailRect)
        elif self.snake[1].y < self.snake[0].y:
            screen.blit(tail_down_surface, tailRect)
        elif self.snake[1].x < self.snake[0].x:
            screen.blit(tail_right_surface, tailRect)
        else:
            screen.blit(tail_right_surface, tailRect)

        for i in range(1, len(self.snake) - 1):
            segment = self.snake[i]
            prev_seg = self.snake[i - 1]
            next_seg = self.snake[i + 1]
            if prev_seg.x == next_seg.x:
                bodySurface = body_vertical_surface
            elif prev_seg.y == next_seg.y:
                bodySurface = body_horizontal_surface
            else:
                bodySurface = body_horizontal_surface
            segmentRect = (segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
            screen.blit(bodySurface, segmentRect)
        if self.direction == Vector2(1,0):
          head_surface = pygame.image.load("graphics/head_right.png")
        elif self.direction == Vector2(0,1):
          head_surface = pygame.image.load("graphics/head_down.png")
        elif self.direction == Vector2(0,-1):
          head_surface = pygame.image.load("graphics/head_up.png")
        elif self.direction == Vector2(-1,0):
          head_surface = pygame.image.load("graphics/head_left.png")
        screen.blit(head_surface, headRect)

    def move(self):
        if self.add_segment:
            self.add_segment = False
        else:
            self.snake = self.snake[1:] # remove tail
        self.snake.append(self.snake[-1] + self.direction)  # add new head
        self.head = [self.snake[-1]]
        self.body = self.snake[1:-1]
        self.tail = [self.snake[0]]
    def reset(self):
        self.snake = [Vector2(4, 4), Vector2(5, 4), Vector2(6, 4), Vector2(7, 4)]
        self.head = [self.snake[-1]]
        self.body = [self.snake[1:-1]]
        self.tail = [self.snake[0]]
        self.direction = Vector2(1, 0)





class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.snake)
        self.state = "running"
        self.score = 0
    def draw(self):
        self.food.draw()
        self.snake.draw()
        current_cells_x = screen.get_width()
        current_cells_y = screen.get_height()
        border_rect = pygame.rect.Rect(0, 0, current_cells_x, current_cells_y)
        pygame.draw.rect(screen, border_colour, border_rect, 5)
    def move(self):
        if self.state == "running":
            self.check_collision_with_food()
            self.snake.move()
            self.check_collision_with_edges()
            self.check_collision_with_self()
    def check_collision_with_food(self):
        if self.snake.snake[-1] == self.food.position:
            print("collision with food")
            self.food.position = self.food.generate_random_pos(self.snake.snake)
            self.score += 1
            self.snake.add_segment = True
    def check_collision_with_edges(self):
        current_cells_x = screen.get_width() // cell_size
        current_cells_y = screen.get_height() // cell_size
        if self.snake.snake[-1].x == current_cells_x or self.snake.snake[-1].x == -1:
            self.game_over()
        if self.snake.snake[-1].y == current_cells_y or self.snake.snake[-1].y == -1:
            self.game_over()
    def check_collision_with_self(self):
        if self.snake.snake[-1] in self.snake.snake[:-1]:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.snake)
        self.state = "stopped"
        self.score = 0

food_surface = pygame.image.load("graphics/apple.png")

tail_left_surface = pygame.image.load("graphics/tail_left.png")
tail_up_surface = pygame.image.load("graphics/tail_up.png")
tail_down_surface = pygame.image.load("graphics/tail_down.png")
tail_right_surface = pygame.image.load("graphics/tail_right.png")
head_surface = pygame.image.load("graphics/head_right.png")
body_horizontal_surface = pygame.image.load("graphics/body_horizontal.png")
body_vertical_surface = pygame.image.load("graphics/body_vertical.png")


info = pygame.display.Info()

screen = pygame.display.set_mode((cell_size * number_of_cells, cell_size * number_of_cells), pygame.RESIZABLE)
pygame.display.set_caption("ML Snake")
game =  Game()
clock = pygame.time.Clock()

snake_update = pygame.USEREVENT
pygame.time.set_timer(snake_update, 100)

while True:
    for event in pygame.event.get():
        if event.type == snake_update:
            game.move()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0,1) or event.key == pygame.K_w and game.snake.direction != Vector2(0,1):
                game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,-1) or event.key == pygame.K_s and game.snake.direction != Vector2(0,-1):
                game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,0) or event.key == pygame.K_d and game.snake.direction != Vector2(-1,0):
                game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,0) or event.key == pygame.K_a and game.snake.direction != Vector2(1,0):
                game.snake.direction = Vector2(-1,0)
            if game.state == "stopped" and event.key == pygame.K_SPACE:
                game.state = "running"
    screen.fill(backgroundColour)

    game.draw()

    pygame.display.update()
    clock.tick(60)

