import socket
import threading
import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics\\head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics\\head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics\\head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics\\head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics\\tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics\\tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics\\tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics\\tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics\\body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics\\body_horizontal.png').convert_alpha()
        
        self.body_tr = pygame.image.load('Graphics\\body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics\\body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics\\body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics\\body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound("Sound\\crunch.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        if head_relation == Vector2(-1,0):
            self.head = self.head_right
        if head_relation == Vector2(0,1):
            self.head = self.head_up
        if head_relation == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        if tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        if tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        if tail_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
    
    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Button:
    def __init__(self, text, pos, font, bg_color, text_color, action):
        self.text = text
        self.pos = pos
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action
        self.rect = pygame.Rect(pos[0], pos[1], 200, 50)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=10)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.action()

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collizion()
        self.check_fail()

    def draw_element(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collizion(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        global high_score, game_active
        current_score = len(self.snake.body) - 3
        if current_score > high_score:
            high_score = current_score
        self.snake.reset()
        game_active = False

    def draw_grass(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
                            
    def draw_score(self):
        score = len(self.snake.body) - 3
        score_text = str(score)
        score_surface = game_font.render(score_text, True, (56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167,209,61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect, 2)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load("Graphics\\apple.png").convert_alpha()
game_font = pygame.font.Font("Font\\PoetsenOne-Regular.ttf", 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 250)

game_active = False
high_score = 0
main_game = None  
start_button = Button("Iniciar Jogo", (200, 350), game_font, (0,255,0), (255,255,255), lambda: start_game())


def start_game():
    global game_active, main_game
    game_active = True
    main_game = MAIN()

def receive_data():
    while True:
        data, client_address = server_socket.recvfrom(1024)  # Bloqueia até receber dados
        face_looks = data.decode()  # Converte os bytes para string
        print(f"Recebido de {client_address}: Direção {face_looks}")

        if face_looks == "Up":
            if main_game and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0,-1)
        if face_looks == "Left":
            if main_game and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1,0)
        if face_looks == "Down":
            if main_game and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0,1)
        if face_looks == "Right":
            if main_game and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1,0)

# Configuração do servidor UDP
SERVER_ADDRESS = ("127.0.0.1", 7070)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(SERVER_ADDRESS)
print(f"Servidor UDP escutando em {SERVER_ADDRESS}...")

thread = threading.Thread(target=receive_data, daemon=True)
thread.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_active:
            start_button.check_click(event)
        else:
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
    
    screen.fill((175,215,70))
    if game_active:
        main_game.draw_element()
    else:
        start_button.draw(screen)

        font = pygame.font.Font("Font\\PoetsenOne-Regular.ttf", 80)  
        title_surface = font.render("Snake Game", True, (255, 255, 255))  
        title_rect = title_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2.5))
        screen.blit(title_surface, title_rect)

        high_score_text = game_font.render(f"Melhor Pontuação: {high_score}", True, (255,255,255))
        score_rect = title_surface.get_rect(topleft=(cell_number * cell_size // 2, cell_number * cell_size // 12))
        screen.blit(high_score_text, score_rect)

    
    pygame.display.update()
    clock.tick(60)
