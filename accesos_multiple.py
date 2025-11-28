import pygame
import sys
import math
import random

pygame.init()
WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME MANTOS")

# Colores
WHITE=(255,255,255)
BLACK=(0,0,0)
GRAY=(120,120,120)
RED=(240,60,60)
GREEN=(60,230,120)
BLUE=(80,140,255)
YELLOW=(245,245,80)
CYAN=(80,255,255)

font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 60)

# Estados del menú
MENU = True
SDMA = False
CDMA = False
INSTRUCTIONS = False

# --- SDMA CONFIG ---
antenna_pos = (WIDTH//2, HEIGHT//2)
beam_angle = 0
beam_speed = 1.5  # velocidad de giro del haz
beam_width = 40   # ancho del haz en grados

# Usuario SDMA
user_sdma = pygame.Rect(100, 100, 40, 40)
user_speed = 4

# Ángulo objetivo del usuario
target_angle = random.randint(0, 359)

# --- CDMA CONFIG (simple) ---
cdma_message = "110011"
cdma_index = 0
cdma_correct = 0
cdma_total = 0

def angle_between_points(cx, cy, px, py):
    ang = math.degrees(math.atan2(py - cy, px - cx))
    return (ang + 360) % 360

# ---------------- MENU ----------------
def draw_menu():
    win.fill(BLACK)
    title = bigfont.render("GAME MANTOS", True, WHITE)
    opt1 = font.render("1 - SDMA (Antena giratoria)", True, WHITE)
    opt2 = font.render("2 - CDMA (Secuencia de código)", True, WHITE)
    opt3 = font.render("3 - Instrucciones", True, WHITE)
    opt4 = font.render("4 - Salir", True, WHITE)

    win.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    win.blit(opt1, (WIDTH//2 - opt1.get_width()//2, 260))
    win.blit(opt2, (WIDTH//2 - opt2.get_width()//2, 310))
    win.blit(opt3, (WIDTH//2 - opt3.get_width()//2, 360))
    win.blit(opt4, (WIDTH//2 - opt4.get_width()//2, 410))
    pygame.display.update()

# -------------- INSTRUCCIONES ---------------
def draw_instructions():
    win.fill(BLACK)
    lines = [
        "INSTRUCCIONES DE JUEGO",
        "",
        "SDMA (Antena giratoria):",
        "- Una antena gira enviando un haz (sector).",
        "- El usuario aparece en la pantalla.",
        "- Su misión: moverlo para que entre al sector correcto.",
        "- Cada usuario tiene un ángulo objetivo.",
        "- Si entra en otro sector → Interferencia.",
        "",
        "CDMA:",
        "- Aparecen bits (0 o 1).",
        "- Presiona la tecla correcta cuando aparezca.",
        "- Bits correctos → señal fuerte.",
        "",
        "Presiona M para volver al menú."
    ]

    y = 50
    for line in lines:
        txt = font.render(line, True, WHITE)
        win.blit(txt, (40, y))
        y += 40

    pygame.display.update()

# ---------------- SDMA GAME ----------------
def draw_sdma():
    global beam_angle

    win.fill(GRAY)

    # Girar el haz
    beam_angle = (beam_angle + beam_speed) % 360

    # Dibujar antena
    pygame.draw.circle(win, YELLOW, antenna_pos, 25)

    # Dibujar sector del haz
    end_x = antenna_pos[0] + 500 * math.cos(math.radians(beam_angle))
    end_y = antenna_pos[1] + 500 * math.sin(math.radians(beam_angle))

    pygame.draw.line(win, CYAN, antenna_pos, (end_x, end_y), 6)

    # Usuario
    pygame.draw.rect(win, BLUE, user_sdma)

    # Visualizar ángulo objetivo
    txt = font.render(f"Ángulo objetivo: {target_angle}°", True, WHITE)
    win.blit(txt, (20, 20))

    # Calcular ángulo actual del usuario
    u_angle = angle_between_points(antenna_pos[0], antenna_pos[1], user_sdma.centerx, user_sdma.centery)

    # Mostrar ángulo del usuario
    a2 = font.render(f"Ángulo usuario: {int(u_angle)}°", True, WHITE)
    win.blit(a2, (20, 60))

    # Comprobar si está en el haz correcto
    diff = abs(u_angle - target_angle)
    diff = min(diff, 360 - diff)  # corrección circular

    if diff < beam_width:
        msg = font.render("Correcto: Usuario en su sector", True, GREEN)
    else:
        msg = font.render("Interferencia: Sector incorrecto", True, RED)

    win.blit(msg, (20, 120))

    pygame.display.update()

# ---------------- CDMA GAME ----------------
def draw_cdma():
    global cdma_index, cdma_correct, cdma_total

    win.fill((40,40,40))

    title = bigfont.render("CDMA - Señal Codificada", True, WHITE)
    win.blit(title, (WIDTH//2 - title.get_width()//2, 80))

    current_bit = cdma_message[cdma_index]

    txt = font.render(f"Bit actual: {current_bit}", True, CYAN)
    win.blit(txt, (WIDTH//2 - txt.get_width()//2, 220))

    score = font.render(f"Aciertos: {cdma_correct} / {cdma_total}", True, WHITE)
    win.blit(score, (WIDTH//2 - score.get_width()//2, 300))

    inst = font.render("Presiona 0 o 1", True, WHITE)
    win.blit(inst, (WIDTH//2 - inst.get_width()//2, 380))

    pygame.display.update()

# ----------------- LOOP PRINCIPAL -----------------
running = True
while running:

    if MENU:
        draw_menu()
    if INSTRUCTIONS:
        draw_instructions()
    if SDMA:
        draw_sdma()
    if CDMA:
        draw_cdma()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- MENU ----------
        if MENU and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                MENU = False; SDMA = True
            elif event.key == pygame.K_2:
                MENU = False; CDMA = True
            elif event.key == pygame.K_3:
                MENU = False; INSTRUCTIONS = True
            elif event.key == pygame.K_4:
                pygame.quit(); sys.exit()

        # ------ INSTRUCCIONES ------
        if INSTRUCTIONS and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                INSTRUCTIONS = False
                MENU = True

        # -------- SDMA ----------
        if SDMA:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: user_sdma.y -= user_speed
            if keys[pygame.K_s]: user_sdma.y += user_speed
            if keys[pygame.K_a]: user_sdma.x -= user_speed
            if keys[pygame.K_d]: user_sdma.x += user_speed

            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                SDMA = False
                MENU = True

        # -------- CDMA ----------
        if CDMA and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0 or event.key == pygame.K_1:
                user_bit = "0" if event.key == pygame.K_0 else "1"
                cdma_total += 1
                if user_bit == cdma_message[cdma_index]:
                    cdma_correct += 1

                cdma_index = (cdma_index + 1) % len(cdma_message)

            if event.key == pygame.K_m:
                CDMA = False
                MENU = True

pygame.quit()
