import pygame
from pygame.locals import*
import os
from random import randrange

pygame.init()     #inicializa o pygame

#Função que faz a cobra crescer
def aumenta_cobra(corpo_cobra):
	for xy in corpo_cobra:
		pygame.draw.rect(JANELA, BRANCO, (xy[0], xy[1], TAMANHO, TAMANHO))

#Função para escrever na tela
def texto_jogo(msg, cor, tam, x, y):
	FONTE = pygame.font.Font("Fontes/Retro Gaming/Retro-Gaming.ttf", tam)
	texto = FONTE.render(msg, True, cor)
	JANELA.blit(texto, texto.get_rect(center = [x, y]))

def reiniciar_jogo():
	global comprimento_cobra, pos_cobra_x, pos_cobra_y, pos_comida_x, pos_comida_y, lista_cobra, corpo_cobra, game_over, pontos
	
	comprimento_cobra = 4
	pos_cobra_x = randrange(0, LARGURA - TAMANHO, 20)
	pos_cobra_y = randrange(0, ALTURA - TAMANHO, 20) 
	pos_comida_x = randrange(0, LARGURA - TAMANHO, 20)
	pos_comida_y = randrange(0, ALTURA - TAMANHO, 20)
	lista_cobra = []
	corpo_cobra = []
	game_over = False
	pontos = 0

#Constante da Janela - Largura e Altura
LARGURA = 500
ALTURA = 500

#Constante das Cores - Fundo, Cobra e Comida
PRETO = (0,0,0)
BRANCO = (255,255,255)
VERMELHO = (255,0,0)
CINZA_ESCURO = (28,28,28)
CINZA_CLARO = (54,54,54)

#Tamanho dos Objetos na Tela
TAMANHO = 20

LOCAL_PLACAR = 40 #Local para escrever o placar do jogo

pygame.display.set_caption("Snake")     #Título do Jogo
JANELA = pygame.display.set_mode((LARGURA, ALTURA))   #Cria a janela

#Posição da Cobra e Comida de Forma Aleatoria
pos_cobra_x = randrange(0, LARGURA - TAMANHO, TAMANHO)
pos_cobra_y = randrange(0, ALTURA - TAMANHO - LOCAL_PLACAR, TAMANHO)
pos_comida_x = randrange(0, LARGURA - TAMANHO, TAMANHO)
pos_comida_y = randrange(0, ALTURA - TAMANHO - LOCAL_PLACAR, TAMANHO)

#Velocidade inicial da cobra
vel_x = 0
vel_y = 0

#Som da colisão
som = pygame.mixer.Sound("coin.wav")

#Lista da cobra
corpo_cobra = []

pontos = 0
comprimento_cobra = 4
game_over = False

#Frame do jogo
relogio = pygame.time.Clock()
FPS = 20

while True:

	relogio.tick(FPS)

	JANELA.fill(PRETO)  #Fundo Preto
	
	#==========Loop Principal==============
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
	#======================================	

	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_UP and vel_y != TAMANHO:
			vel_y = - TAMANHO
			vel_x = 0
		if event.key == pygame.K_DOWN and vel_y != - TAMANHO:
			vel_y = TAMANHO
			vel_x = 0
		if event.key == pygame.K_LEFT and vel_x != TAMANHO:
			vel_x = - TAMANHO
			vel_y = 0
		if event.key == pygame.K_RIGHT and vel_x != - TAMANHO:
			vel_x = TAMANHO
			vel_y = 0			
	
	#atualiza depois de pressionar os setas (precisa ficar fora do for)			
	pos_cobra_x += vel_x
	pos_cobra_y += vel_y		

	#atravessar a borda e aparecer do outro lado
	if pos_cobra_x + TAMANHO > LARGURA:
		pos_cobra_x = 0
	if pos_cobra_x < 0:
		pos_cobra_x = LARGURA - TAMANHO

	if pos_cobra_y + TAMANHO > ALTURA - LOCAL_PLACAR:
		pos_cobra_y = 0
	if pos_cobra_y < 0:
		pos_cobra_y = ALTURA - TAMANHO - LOCAL_PLACAR

	#Desenho da Cobra e Comida
	cobra = pygame.draw.rect(JANELA, BRANCO, (pos_cobra_x, pos_cobra_y, TAMANHO, TAMANHO))
	comida = pygame.draw.rect(JANELA, VERMELHO, (pos_comida_x, pos_comida_y, TAMANHO, TAMANHO))
	
	#Função que verifica a colisão da cobra com a comida, executa o som, gerencia o comprimento da cobra e computa os pontos
	if cobra.colliderect(comida):
		pos_comida_x = randrange(0, LARGURA - TAMANHO, TAMANHO)
		pos_comida_y = randrange(0, LARGURA - TAMANHO - LOCAL_PLACAR, TAMANHO)
		som.play()
		comprimento_cobra = comprimento_cobra + 1
		pontos = pontos + 1

	#Cria uma lista dentro da lista	
	cobra_cabeca = []
	cobra_cabeca.append(pos_cobra_x)
	cobra_cabeca.append(pos_cobra_y)
	corpo_cobra.append(cobra_cabeca)

	#Evita da cobra crescer sozinha 
	if len(corpo_cobra) > comprimento_cobra:
		del corpo_cobra[0]

	#Verifica a colisão da cobra com ela mesma	
	if any (corpo == cobra_cabeca for corpo in corpo_cobra[:-4]):
		game_over = True

		while game_over:
			JANELA.fill(PRETO)
					
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						reiniciar_jogo()

			texto_jogo("GAME OVER", BRANCO, 40, LARGURA//2, ALTURA//2 - 160)
			texto_jogo("Pontuação Final: " + str(pontos), BRANCO, 30, LARGURA//2, ALTURA//2)
			texto_jogo("Play Again, press R", BRANCO, 30, LARGURA//2, ALTURA//2 + 100)

			pygame.display.update()

	aumenta_cobra(corpo_cobra)	
	
	#Desenha o Local do Placar e Escreve a pontuação
	pygame.draw.rect(JANELA, CINZA_ESCURO, [0, ALTURA - LOCAL_PLACAR, LARGURA, 40])	
	texto_jogo("Pontos: " + str(pontos), BRANCO, 30, 100, ALTURA - 20)
	
	pygame.display.update() #Atualiza a Tela
