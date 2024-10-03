import py5
import random

# Variables globales
paddle1_y = paddle2_y = 0
paddle_width = paddle_height = 0
paddle_speed = ball_size = 0
ball_x = ball_y = ball_dx = ball_dy = 0
player1_score = player2_score = 0
background_image= None
backround_image2= None

# Estado de las teclas presionadas
keys = set()
game_mode= None
menu_active= True
error_probability = 0.75
winning_score = 5
winner = None
def setup():
     py5.size(640, 359)
     global paddle_width, paddle_height, paddle_speed, ball_size
     global ball_x, ball_y, ball_dx, ball_dy
     global paddle1_y, paddle2_y, player1_score, player2_score, backround_image2, background_image
     

     background_image = py5.load_image("bola.jpg")  # Cambia "fondo.jpg" por tu archivo
     backround_image2 = py5.load_image("sd.jpg")
   

     paddle_width = 20
     paddle_height = 100
     paddle_speed = 7
     ball_size = 20

     reset_game()

def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx = 5
    ball_dy = 3
    paddle1_y = py5.height / 2 - paddle_height / 2
    paddle2_y = py5.height / 2 - paddle_height / 2
    player1_score = 0
    player2_score = 0
    winner = None

def draw():
     global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
     global player1_score, player2_score, menu_active, game_mode, background_image 

     if background_image is not None:
      py5.image(background_image, 0, 0, py5.width, py5.height)

     if menu_active:
        draw_menu()  # Dibujar el menú principal
     else:
         if winner is None:
            draw_game()  # Dibujar el juego si no hay ganador
         else:
            draw_winner() 


def draw_menu():
     global backround_image2
     
     # Dibujar la imagen de fondo del menú
     if backround_image2 is not None:
        py5.image(backround_image2, 0, 0, py5.width, py5.height)  # Dibuja la imagen cubriendo toda la pantalla
     else:
        py5.background(0)  # Si no se carga, usa un color de fondo

     py5.text_align(py5.CENTER)
     py5.text_size(32)
     py5.text("Pong Game", py5.width / 2, py5.height / 3)
     py5.text_size(24)
     py5.text("Presiona 1 para jugar contra la computadora", py5.width / 2, py5.height / 2)
     py5.text("Presiona 2 para jugar multijugador", py5.width / 2, py5.height / 2 + 40)
     py5.text_size(28)
     py5.text("Ganará el primer jugador que llegue a los 5 puntos!", py5.width / 2, py5.height / 1.07)


def draw_game():
    global ball_x, ball_y, ball_dx, ball_dy, paddle1_y, paddle2_y
    global player1_score, player2_score 

    # Dibujar los paddles
    py5.fill(0, 0, 0)
    py5.stroke(255)
    py5.rect(30, paddle1_y, paddle_width, paddle_height)  # Pala izquierda
    py5.fill(0, 0, 0)
    py5.stroke(255)
    py5.rect(py5.width - 30 - paddle_width, paddle2_y, paddle_width, paddle_height)  # Pala derecha
    # Dibujar la pelota
    py5.ellipse(ball_x, ball_y, ball_size, ball_size)
    
    # Dibujar el marcador
    py5.text_size(32)
    py5.text_align(py5.CENTER)
    py5.fill(255)
    py5.text(f"{player1_score} - {player2_score}", py5.width / 2, 40)
    
    # Dibujar ayuda de teclas
    py5.text_size(16)
    py5.text_align(py5.LEFT)
    py5.fill(255)
    py5.text("Jugador 1: W (Arriba), S (Abajo)", 10, 30)
    py5.text_align(py5.RIGHT)
    py5.text("Jugador 2:  ↑ (Arriba),  ↓ (Abajo)", py5.width - 10, 30)
    
    # Actualizar posición de la pelota
    ball_x += ball_dx
    ball_y += ball_dy
    
    # Rebote de la pelota en la parte superior e inferior
    if ball_y <= ball_size / 2 or ball_y >= py5.height - ball_size / 2:
        ball_dy *= -1
    
    # Verificar colisiones con los paddles
    if ball_x - ball_size / 2 <= 30 + paddle_width:
        if paddle1_y < ball_y < paddle1_y + paddle_height:
            ball_dx *= -1
            ball_x = 30 + paddle_width + ball_size / 2
    
    if ball_x + ball_size / 2 >= py5.width - 30 - paddle_width:
        if paddle2_y < ball_y < paddle2_y + paddle_height:
            ball_dx *= -1
            ball_x = py5.width - 30 - paddle_width - ball_size / 2
    if ball_x + ball_size / 2 >= py5.width - 30 - paddle_width:

        # Aquí agregamos la probabilidad de error
         if random.random() > error_probability:  # La computadora intenta interceptar
            if paddle2_y < ball_y < paddle2_y + paddle_height:
                ball_dx *= -1
                ball_x = py5.width - 30 - paddle_width - ball_size / 2
    
    # Si la pelota sale por la izquierda
    if ball_x < 0:
        player2_score += 1
        reset_ball()
    
    # Si la pelota sale por la derecha
    if ball_x > py5.width:
        player1_score += 1
        reset_ball()

    if player1_score >= winning_score:
        winner = "Jugador 1"
        print("el jugador 1 ha ganado")
        reset_game()
    elif player2_score >= winning_score:
        winner = "Jugador 2"
        print("el jugador 2 ha ganado")
        reset_game()

    # Limitar el movimiento de los paddles
    if game_mode == 'multi' or game_mode == 'single':
        if 'w' in keys and paddle1_y > 0:
            paddle1_y -= paddle_speed
        if 's' in keys and paddle1_y < py5.height - paddle_height:
            paddle1_y += paddle_speed
        if game_mode == 'multi':
            if py5.UP in keys and paddle2_y > 0:
                paddle2_y -= paddle_speed
            if py5.DOWN in keys and paddle2_y < py5.height - paddle_height:
                paddle2_y += paddle_speed
        elif game_mode == 'single':
         # Mover el paddle de la computadora (simple IA)
         if random.random() > error_probability:  # La computadora intenta interceptar
             if ball_y < paddle2_y + paddle_height / 2:
                paddle2_y -= paddle_speed
             elif ball_y > paddle2_y + paddle_height / 2:
                paddle2_y += paddle_speed

def draw_winner():
    py5.background(0)  # Fondo negro
    py5.text_align(py5.CENTER)
    py5.text_size(32)
    py5.fill(255)
    py5.text(f"{winner} ha ganado!", py5.width / 2, py5.height / 2 - 20)
    py5.text_size(24)
    py5.text("Presiona R para reiniciar", py5.width / 2, py5.height / 2 + 20)


def key_pressed():
    global keys, game_mode, menu_active
    if menu_active:
        if py5.key == '1':
            game_mode = 'single'
            menu_active = False
        elif py5.key == '2':
            game_mode = 'multi'
            menu_active = False
    else:
        keys.add(py5.key)
def key_released():
    global keys
    keys.discard(py5.key_code)
    keys.discard(py5.key)

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = py5.width / 2
    ball_y = py5.height / 2
    ball_dx *= -1
    ball_dy = py5.random(-3, 3)

if __name__ == "__main__":
    py5.run_sketch()
