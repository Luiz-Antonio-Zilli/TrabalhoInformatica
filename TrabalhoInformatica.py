import pygame
import random

# Inicialização do Pygame
pygame.init()

# Configuração da janela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Simples")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configuração do jogador (nave)
player_width, player_height = 50, 30
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Configuração dos tiros
bullet_width, bullet_height = 5, 10
bullets = []
bullet_speed = -7

# Configuração dos inimigos
enemy_width, enemy_height = 40, 30
enemy_speed = 2
enemy_move_down = 40
enemies = []
rows, cols = 3, 7
wave = 1  # Contador de ondas

# Configuração dos tiros dos inimigos
enemy_bullet_width, enemy_bullet_height = 5, 10
enemy_bullets = []
enemy_bullet_speed = 7  # Velocidade dos tiros dos inimigos
enemy_fire_rate = 30  # A cada 30 quadros, um inimigo pode disparar

# Variáveis do jogo
score = 0
font = pygame.font.Font(None, 36)
running = True
clock = pygame.time.Clock()

# Funções auxiliares
def draw_player():
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))

def draw_enemies():
    for enemy in enemies:
        color = random.choice([GREEN, (255, 255, 0)])  # Alterna entre verde e amarelo
        pygame.draw.rect(screen, color, (enemy[0], enemy[1], enemy_width, enemy_height))

def draw_enemy_bullets():
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height))

def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    wave_text = font.render(f"Wave: {wave}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(wave_text, (WIDTH - 150, 10))

def create_enemies():
    global enemy_speed
    for row in range(rows):
        for col in range(cols):
            enemy_x = col * (enemy_width + 20) + 50
            enemy_y = row * (enemy_height + 20) + 50
            enemies.append([enemy_x, enemy_y])
    enemy_speed += 0.5  # Incrementa a dificuldade a cada nova onda

# Função para fazer os inimigos atirarem
def enemy_shoot():
    for enemy in enemies:
        if random.randint(1, enemy_fire_rate) == 1:  # Chance de 1 em "enemy_fire_rate"
            enemy_bullets.append([enemy[0] + enemy_width // 2 - enemy_bullet_width // 2, enemy[1] + enemy_height])

# Função para verificar colisões dos tiros dos inimigos com o jogador
def check_enemy_bullet_collisions():
    global running
    for bullet in enemy_bullets[:]:
        if (bullet[0] < player_x + player_width and
            bullet[0] + enemy_bullet_width > player_x and
            bullet[1] < player_y + player_height and
            bullet[1] + enemy_bullet_height > player_y):
            # Colisão com o jogador
            running = False  # Fim do jogo
            enemy_bullets.remove(bullet)  # Remover o tiro que colidiu com o jogador

# Inicializar os inimigos
create_enemies()

# Loop principal do jogo
while running:
    screen.fill(BLACK)
    
    # Eventos do Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Limite de tiros na tela
            bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])

    # Atualizar tiros
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Atualizar inimigos
    move_direction = 1
    for enemy in enemies:
        enemy[0] += enemy_speed * move_direction
        if enemy[0] > WIDTH - enemy_width or enemy[0] < 0:
            enemy_speed *= -1
            for e in enemies:
                e[1] += enemy_move_down
            break

    # Verificar colisões
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if (enemy[0] < bullet[0] < enemy[0] + enemy_width and
                enemy[1] < bullet[1] < enemy[1] + enemy_height):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Verificar se todos os inimigos foram eliminados
    if not enemies:
        wave += 1
        create_enemies()

    # Fim do jogo
    for enemy in enemies:
        if enemy[1] + enemy_height > player_y:
            running = False

    # Fazer os inimigos atirarem
    enemy_shoot()

    # Atualizar tiros dos inimigos
    for bullet in enemy_bullets[:]:
        bullet[1] += enemy_bullet_speed
        if bullet[1] > HEIGHT:
            enemy_bullets.remove(bullet)

    # Verificar colisões dos tiros dos inimigos com o jogador
    check_enemy_bullet_collisions()

    # Desenhar objetos na tela
    draw_player()
    draw_bullets()
    draw_enemies()
    draw_enemy_bullets()  # Desenhar os tiros dos inimigos
    display_score()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()





