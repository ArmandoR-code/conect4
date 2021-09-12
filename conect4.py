"""
Juego de tablero Conecta 4 para el modulo de pyhton de Bedu
Idea de un tutorial de FreeCampCode
Por Army-R Code
"""

import numpy as np # Modulo matemático, nos ayuda para crear matices
import pygame as pg # Modulo para la creacion de juegos
import sys
import math

# Variables globales
ROW_COUNT = 6 
COL_COUNT = 7 
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Creamos el tablero con una matriz de 6 filas x 7 columnas
def create_board():
	board = np.zeros((ROW_COUNT, COL_COUNT))
	return board

def drop_coin(board, row, movement, coin):
	board[row][movement] = coin
	
def valid_movement(board, movement): 
	# Funcion para validar que la ficha entre en algún lugar existente en la matriz
	return board[ROW_COUNT-1][movement] == 0 
	""" ROW_COUNT-1 = 5, representa el numero de fila empezando de abajo acia arriba, i.e. la última fila, y movement representa la selección del jugador (la columna); mientras estas sea igual a 0, i.e. este libre, puede tirar la ficha """

def available_space(board, movement):
	for r in range(ROW_COUNT):
		if board[r][movement] == 0:
			return r

def print_board(board): # Función para cambiar la orientación de la matriz
	print(np.flip(board, 0))
"""
Nota: Mejorar la fucion winning_palyer
"""
def winning_player(board, coin):
	# Revisar todas las posiciones horizontales
	for c in range(COL_COUNT-3): # Después de la 3era columna no es posible conectar 4
		for r in range(ROW_COUNT):
			if board[r][c] == coin and board[r][c+1] == coin and board[r][c+2] == coin and board[r][c+3] == coin:
				return True
	# Revisar todas las posiciones verticales
	for c in range(COL_COUNT): 
		for r in range(ROW_COUNT-3): # Después de la 3era fila no es posible conectar 4
			if board[r][c] == coin and board[r+1][c] == coin and board[r+2][c] == coin and board[r+3][c] == coin:
				return True	
	# Revisar todas las posiciones diagonales positivas
	for c in range(COL_COUNT-3): 
		for r in range(ROW_COUNT-3):
			if board[r][c] == coin and board[r+1][c+1] == coin and board[r+2][c+2] == coin and board[r+3][c+3] == coin:
				return True					
	# Revisar todas las posiciones diagonales negativas
	for c in range(COL_COUNT-3): 
		for r in range(3, ROW_COUNT):
			if board[r][c] == coin and board[r-1][c+1] == coin and board[r-2][c+2] == coin and board[r-3][c+3] == coin:
				return True	 			
"""
Nota: Mejorar la funcion draw_board
"""
def draw_board(board):
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT):
			# Dibujamos el rectangulo que fungira como fondo en el juego
			pg.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			# Dibujamos los espacios vacios
			pg.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS) # pygame solo acepta valores int
		
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
					# Dibujamos la ficha color rojo
					pg.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2:
				# Dibujamos la ficha colo amarillo
				pg.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)			
	pg.display.update()			

board = create_board() # Desplegamos el tablero
print_board(board)

turn = 0 # Variable para asignar el turno al jugador

game_over = False # El juego no termina hasta que game_over sea igual a True

pg.init()

# Determinar el tamaño de la pantalla (tablero)
SQUARESIZE = 100

width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE # Se añade un espacio más para mover las fichas en la parte superior

size = (width, height)

RADIUS = int(SQUARESIZE/2-5) # Define el tamaño de los circulos para las fichas

screen = pg.display.set_mode(size)
draw_board(board)
pg.display.update()

font = pg.font.SysFont("monospace", 50) # Dfine la fuente a usar en el mensaje ganador

while not game_over:
	for event in pg.event.get():
		if event.type == pg.QUIT: # Evento para salir del juego
			sys.exit()
		
		if event.type == pg.MOUSEMOTION: # Evento para dejar caer la ficha
			pg.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pg.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else:
				pg.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)	
		
		pg.display.update()

		if event.type == pg.MOUSEBUTTONDOWN: # Evento para dar click sobre la casilla
			pg.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE)) # Permite visualizar por completo el mensaje ganador

			# Turno del Jugador 1
			if turn == 0:
				posx = event.pos[0]
				movement = int(math.floor(posx / SQUARESIZE))
				
				if valid_movement(board, movement):
					row = available_space(board, movement)
					drop_coin(board, row, movement, 1)

					if winning_player(board, 1):
						# Desplegamos mensaje ganador en el tablero
						label = font.render("¡¡Gana el Jugador 1!!", 1, RED)
						screen.blit(label, (40, 10))
						game_over = True
						
			# Turno del Jugador 2
			else:
				posx = event.pos[0]
				movement = int(math.floor(posx / SQUARESIZE))
				
				if valid_movement(board, movement):
					row = available_space(board, movement)
					drop_coin(board, row, movement, 2)

					if winning_player(board, 2):
						label = font.render("¡¡Gana el Jugador 2!!", 2, YELLOW)
						screen.blit(label, (40, 10))
						game_over = True			
				
			print_board(board)
			draw_board(board)
			# turn += 1 y tunr %= 2 sirven para cambiar el valor de turn de 1 a 0
			turn += 1
			turn %= 2 

			if game_over:
				pg.time.wait(3000) # Tiempo que espera antes de cerrar el juego. Milisegundos

		
