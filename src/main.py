import pygame
import random
import sys
import sqlite3
from datetime import datetime
from utils.logger import setup_logger, get_logger

# Configuración del logger
setup_logger()
logger = get_logger()

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Sin redimensionable
pygame.display.set_caption("Juego de Avión de Guerra")

# Inicialización de reloj
clock = pygame.time.Clock()
FPS = 60

# Cargar imágenes
player_img = pygame.image.load("assets/player.png")
enemy_img = pygame.image.load("assets/enemy.png")
bullet_img = pygame.image.load("assets/bullet.png")
enemy_bullet_img = pygame.image.load("assets/enemy_bullet.png")

# Escalar imágenes
player_img = pygame.transform.scale(player_img, (60, 50))
enemy_img = pygame.transform.scale(enemy_img, (60, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))
enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (10, 20))

# Variables globales
score = 0
paused = False

# Base de datos
def create_db():
    conn = sqlite3.connect('juego.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puntaje INTEGER,
            fecha TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Base de datos creada o ya existente.")

def save_score(puntaje):
    conn = sqlite3.connect('juego.db')
    c = conn.cursor()
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO resultados (puntaje, fecha) VALUES (?, ?)', (puntaje, fecha))
    conn.commit()
    conn.close()
    logger.info(f'Puntaje guardado: {puntaje} en la fecha {fecha}')

def get_high_scores():
    conn = sqlite3.connect('juego.db')
    c = conn.cursor()
    c.execute('SELECT * FROM resultados ORDER BY fecha DESC')
    scores = c.fetchall()
    conn.close()
    return scores

# Clases del juego
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 60)
        self.speed_x = 3
        self.speed_y = 3
        self.shoot_timer = 0
        self.last_valid_position = self.rect.topleft

    def update(self):
        global WIDTH, HEIGHT

        self.last_valid_position = self.rect.topleft

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        self.avoid_bullets()

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y

        if pygame.sprite.spritecollideany(self, enemies):
            self.rect.topleft = self.last_valid_position
            self.speed_x = -self.speed_x
            self.speed_y = -self.speed_y

        self.shoot_timer += 1
        if self.shoot_timer >= 20:
            self.shoot()
            self.shoot_timer = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def avoid_bullets(self):
        """Evitar balas enemigas cercanas"""
        for bullet in enemy_bullets:
            distance_x = abs(self.rect.centerx - bullet.rect.centerx)
            distance_y = abs(self.rect.centery - bullet.rect.centery)

            if distance_x < 50 and distance_y < 100:
                if bullet.rect.centerx < self.rect.centerx:
                    self.rect.x += self.speed_x
                else:
                    self.rect.x -= self.speed_x

                if bullet.rect.centery > self.rect.centery:
                    self.rect.y -= self.speed_y


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = -7

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()


# Función para reiniciar el juego
def restart_game():
    global all_sprites, enemies, bullets, enemy_bullets, player, score
    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    enemy_bullets.empty()
    score = 0

    player = Player()
    all_sprites.add(player)

    for i in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    logger.info('Juego reiniciado')


# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Inicializar juego
player = None
create_db()
restart_game()

# Bucle principal del juego
running = True
game_over = False
score_saved = False  # Para evitar guardar el puntaje varias veces

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_r and game_over:
                game_over = False
                score_saved = False  # Restablecer el flag cuando reinicia el juego
                restart_game()

    if not paused and not game_over:
        all_sprites.update()

        for enemy in enemies:
            if random.random() < 0.01:
                enemy.shoot()

        if pygame.sprite.spritecollideany(player, enemy_bullets):
            game_over = True

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    font = pygame.font.SysFont("Arial", 30)
    score_text = font.render(f"Puntaje: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    if paused:
        font = pygame.font.SysFont("Arial", 48)
        pause_text = font.render("Pausado. Presiona P para continuar", True, (255, 255, 0))
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(pause_text, pause_rect)

    if game_over:
        if not score_saved:
            save_score(score)
            score_saved = True  # Aseguramos que solo se guarde una vez al perder
            logger.info(f'Fin del juego. Puntaje final: {score}')
        font = pygame.font.SysFont("Arial", 48)
        text = font.render("¡Game Over! Presiona R para reiniciar", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        # Mostrar los mejores puntajes
        high_scores = get_high_scores()
        font = pygame.font.SysFont("Arial", 24)
        y_offset = HEIGHT // 2 + 60
        for idx, (id, puntaje, fecha) in enumerate(high_scores[:5]):
            high_score_text = font.render(f"{idx + 1}. {puntaje} - {fecha}", True, (255, 255, 255))
            screen.blit(high_score_text, (WIDTH // 2 - 150, y_offset + idx * 30))

    pygame.display.flip()

pygame.quit()
sys.exit()
