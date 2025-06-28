import pygame, sys, random, numpy as np, pickle
from pygame import Vector2

pygame.init()

# Basic Colours
foregroundColour = (108, 255, 109)
backgroundColour = (124, 233, 255)
border_colour = (255, 102, 255)
text_colour = (0, 0, 0)

# Grid configuration
cell_size = 30
number_of_cells = 25

#Loading all graphics before the game starts for performance
food_surface = pygame.image.load("graphics/apple.png")
tail_left_surface = pygame.image.load("graphics/tail_left.png")
tail_up_surface = pygame.image.load("graphics/tail_up.png")
tail_down_surface = pygame.image.load("graphics/tail_down.png")
tail_right_surface = pygame.image.load("graphics/tail_right.png")
head_surface = pygame.image.load("graphics/head_right.png")
body_horizontal_surface = pygame.image.load("graphics/body_horizontal.png")
body_vertical_surface = pygame.image.load("graphics/body_vertical.png")

info = pygame.display.Info()

# Creates resizable game window
screen = pygame.display.set_mode((cell_size * number_of_cells, cell_size * number_of_cells), pygame.RESIZABLE)
pygame.display.set_caption("ML Snake")
icon = pygame.image.load("graphics/icon.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Snake update timer (controls speed of game)
snake_update = pygame.USEREVENT
pygame.time.set_timer(snake_update, 100)

# Class that generates food
class Food:
    def __init__(self, snake):
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
            position = self.generate_random_coord() # avoids food generating inside the snake
        return position

# Class that generates snake
class Snake:
    def __init__(self):
        self.snake = [Vector2(4,4), Vector2(5,4), Vector2(6,4), Vector2(7,4)] # initial snake position
        self.head = [self.snake[-1]]
        self.body = self.snake[1:-1]
        self.tail = [self.snake[0]]
        self.direction = Vector2(1,0) # initial direction is to the right
        self.add_segment = False # boolean that decides whether the snake is growing

    def draw(self):
        headRect = (self.head[0].x * cell_size, self.head[0].y * cell_size, cell_size, cell_size)
        tailRect = (self.tail[0].x * cell_size, self.tail[0].y * cell_size, cell_size, cell_size)
        if self.snake[1].x > self.snake[0].x: # draw tail with correct orientation
            screen.blit(tail_left_surface, tailRect)
        elif self.snake[1].y > self.snake[0].y:
            screen.blit(tail_up_surface, tailRect)
        elif self.snake[1].y < self.snake[0].y:
            screen.blit(tail_down_surface, tailRect)
        elif self.snake[1].x < self.snake[0].x:
            screen.blit(tail_right_surface, tailRect)
        else:
            screen.blit(tail_right_surface, tailRect)

        for i in range(1, len(self.snake) - 1): # draw body of snake correctly
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


        if self.direction == Vector2(1,0): # draw head with correct orientation
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
            self.add_segment = False # does not remove tail and disables growth on next move
        else:
            self.snake = self.snake[1:] # remove tail
        self.snake.append(self.snake[-1] + self.direction)  # add new head
        self.head = [self.snake[-1]]
        self.body = self.snake[1:-1]
        self.tail = [self.snake[0]]
    def reset(self):
        # resets the snake to initial position
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
        try: # loads No. of attempts if it exists
            with open("game.attempt.pkl", "rb") as f:
                self.attempt = pickle.load(f)
                print("No. of attempts loaded from file.")
        except FileNotFoundError:
            print("No previous attempts found, starting fresh.")
            self.attempt = 0
        self.cumulative_reward = 0
    def draw(self):
        self.food.draw()
        self.snake.draw()
        current_cells_x = screen.get_width()
        current_cells_y = screen.get_height()
        border_rect = pygame.rect.Rect(0, 0, current_cells_x, current_cells_y)
        pygame.draw.rect(screen, border_colour, border_rect, 5) # draw game borders
        aptos_font = pygame.font.Font("graphics/Aptos.ttf", 50)
        score = aptos_font.render(f"Score: {game.score}", True, text_colour)
        attempt = aptos_font.render(f"Attempts: {game.attempt}", True, text_colour)
        text_rect = score.get_rect()
        text_rect.topleft = (10, 0)
        attempt_rect = attempt.get_rect()
        attempt_rect.topleft = (10, 40)
        screen.blit(score, text_rect)
        screen.blit(attempt, attempt_rect)
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
            self.snake.add_segment = True # allows growth on next move
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
        # saves progress in a pickle and resets the game
        with open("q_table.pkl", "wb") as f:
            pickle.dump(ai.q_table, f)
        with open("game.attempt.pkl", "wb") as f:
            pickle.dump(game.attempt, f)
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.snake)
        self.state = "stopped"
        self.score = 0

class AiSnake:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.5, exploration_decay=0.999):
        # Q-learning parameters
        self.q_table = {}
        self.actions = actions
        self.lr = learning_rate
        self.gamma = discount_factor
        try:
            with open("ai.epsilon.pkl", "rb") as f:
                self.epsilon = pickle.load(f)
                print("Epsilon loaded from file.")
        except FileNotFoundError:
            print("No previous epsilons found, starting fresh.")
            self.epsilon = exploration_rate
        self.epsilon_decay = exploration_decay

    def get_action(self, state):
        # Epsilon-greedy action selection (decides how often the snake makes a random move vs. goes with the best move)
        if random.random() < self.epsilon:
            return random.choice(self.actions)  # Explore
        else:
            q_values = [self.q_table.get((state, a), 0) for a in self.actions]
            return self.actions[np.argmax(q_values)]  # Exploit (returns the best possible action)

    def update(self, state, action, reward, next_state):
        old_value = self.q_table.get((state, action), 0)
        future_values = [self.q_table.get((next_state, a), 0) for a in self.actions]
        future_best = max(future_values)

        new_value = old_value + self.lr * (reward + self.gamma * future_best - old_value)
        self.q_table[(state, action)] = new_value
        self.epsilon *= self.epsilon_decay
        print(len(self.q_table))

# encodes game state into a tuple for Q-learning
def get_state(game):
    head = game.snake.head[0]
    food = game.food.position
    direction = game.snake.direction

    danger_straight = 0
    danger_left = 0
    danger_right = 0

    directions = [Vector2(1,0), Vector2(0,1), Vector2(-1,0), Vector2(0,-1)]
    idx = directions.index(direction)

    for i, offset in enumerate([-1, 0, 1]):
        test_dir = directions[(idx + offset) % 4]
        next_pos = head + test_dir
        if (
            next_pos.x >= number_of_cells or next_pos.x < 0 or
            next_pos.y >= number_of_cells or next_pos.y < 0 or
            next_pos in game.snake.snake
            ):
            if offset == -1: danger_left = 1
            if offset == 0: danger_straight = 1
            if offset == 1: danger_right = 1

    if food.x > head.x:
        food_dir_x = 1
    elif food.x < head.x:
        food_dir_x = -1
    else:
        food_dir_x = 0

    if food.y > head.y:
        food_dir_y = 1
    elif food.y < head.y:
        food_dir_y = -1
    else:
        food_dir_y = 0
    return (
        danger_straight,
        danger_left,
        danger_right,
        int(direction.x), int(direction.y),
        food_dir_x, food_dir_y
        )

ai = AiSnake(actions=["up", "down", "left", "right"])

try:
    with open("q_table.pkl", "rb") as f:
        ai.q_table = pickle.load(f)
        print("Q-table loaded from file.")
except FileNotFoundError:
    print("No Q-table found, starting fresh.")

game =  Game()

# Game Loop For Machine Learning
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("q_table.pkl", "wb") as f:
                pickle.dump(ai.q_table, f)
            with open("game.attempt.pkl", "wb") as f:
                pickle.dump(game.attempt, f)
            with open("ai.epsilon.pkl", "wb") as f:
                pickle.dump(ai.epsilon, f)
            pygame.quit()
            sys.exit()

    if game.state == "running":
        state = get_state(game)
        action = ai.get_action(state)

        # Set direction
        if action == "up" and game.snake.direction != Vector2(0, 1):
            game.snake.direction = Vector2(0, -1)
        elif action == "down" and game.snake.direction != Vector2(0, -1):
            game.snake.direction = Vector2(0, 1)
        elif action == "left" and game.snake.direction != Vector2(1, 0):
            game.snake.direction = Vector2(-1, 0)
        elif action == "right" and game.snake.direction != Vector2(-1, 0):
            game.snake.direction = Vector2(1, 0)

        # Old score before move
        old_score = game.score

        game.move()

        # Compute reward
        if game.state == "stopped":
            game.state = "running"
            reward = -10
            game.attempt += 1
        elif game.score > old_score:
            reward = 10
        else:
            reward = -0.5

        new_state = get_state(game)
        ai.update(state, action, reward, new_state)
### Game Loop for Player Use
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == snake_update:
    #             game.move()
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_UP and game.snake.direction != Vector2(0,
    #                                                                             1) or event.key == pygame.K_w and game.snake.direction != Vector2(
    #                     0, 1):
    #                 game.snake.direction = Vector2(0, -1)
    #             if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0,
    #                                                                               -1) or event.key == pygame.K_s and game.snake.direction != Vector2(
    #                     0, -1):
    #                 game.snake.direction = Vector2(0, 1)
    #             if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1,
    #                                                                                0) or event.key == pygame.K_d and game.snake.direction != Vector2(
    #                     -1, 0):
    #                 game.snake.direction = Vector2(1, 0)
    #             if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1,
    #                                                                               0) or event.key == pygame.K_a and game.snake.direction != Vector2(
    #                     1, 0):
    #                 game.snake.direction = Vector2(-1, 0)
    #             if game.state == "stopped" and event.key == pygame.K_SPACE:
    #                 game.state = "running"
    screen.fill(backgroundColour)
    game.draw()
    pygame.display.update()
    clock.tick(10) # Change to 60 in case of player input


