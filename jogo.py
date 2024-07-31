import pygame
from gerador import gera_numeros
import time

pygame.init()
clock = pygame.time.Clock()
FPS = 30

LARGURA = 800
ALTURA = 500
QUADRADO = 100
CORES = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
COR_PLATAFORMA = (0, 0, 0)

window = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('TESTE NINJA')
fonte = pygame.font.Font(None, 40)

TEMPO_JOGO = 60

def desenha_quadrados(valores, clicado):
    plataforma_rect = pygame.Rect(0, ALTURA - QUADRADO, LARGURA, QUADRADO)
    pygame.draw.rect(window, COR_PLATAFORMA, plataforma_rect)
    for i in range(3):
        quadrado_rect = pygame.Rect((LARGURA//2 - QUADRADO//2, ALTURA//2 - QUADRADO//2 + (i - 1) * QUADRADO), (QUADRADO, QUADRADO))
        if i not in clicado:
            pygame.draw.rect(window, CORES[i], quadrado_rect)
            text = fonte.render(str(valores[i]), True, (0, 0, 0))
            window.blit(text, (quadrado_rect.x + (QUADRADO - text.get_width()) // 2, quadrado_rect.y + (QUADRADO - text.get_height()) // 2))
        else:
            if valores[i] == resposta_certa:
                text = fonte.render("Certo!", True, CORES[1])
            else:
                text = fonte.render("Errado!", True, CORES[0])
            window.blit(text, (quadrado_rect.x + (QUADRADO - text.get_width()) // 2, quadrado_rect.y + (QUADRADO - text.get_height()) // 2))

def tela_jogo():
    global valores, clicado, resposta_certa, proximo_reinicio
    valores = gera_numeros()
    clicado = []
    proximo_reinicio = None
    for v in valores[0:3]:
        if sum(valores[0:3]) - v == valores[3]:
            resposta_certa = v

def tela_inicial():
    global VIDAS, ACERTOS, botao_rect, tempo_inicio, tempo_restante
    VIDAS = 3
    ACERTOS = 0
    tempo_inicio = time.time()
    tempo_restante = TEMPO_JOGO
    window.fill((255, 255, 255))

    BOTAO_LARGURA = 200
    BOTAO_ALTURA = 100
    botao_rect = pygame.Rect(LARGURA // 2 - BOTAO_LARGURA // 2, ALTURA // 2 - BOTAO_ALTURA // 2, BOTAO_LARGURA, BOTAO_ALTURA)
    pygame.draw.rect(window, CORES[0], botao_rect)
    mensagem = fonte.render("JOGAR", True, (255, 255, 255))
    window.blit(mensagem, (LARGURA // 2 - mensagem.get_width() // 2, ALTURA // 2 - mensagem.get_height() // 2))
    pygame.display.update()

def tela_game_over():
    window.fill((255, 255, 255))

    numero_acertos = fonte.render(f"NÚMERO DE ACERTOS: {ACERTOS}", True, (0, 0, 0))
    window.blit(numero_acertos, (LARGURA // 2 - numero_acertos.get_width() // 2, ALTURA // 2 - numero_acertos.get_height() // 2 - 60))

    tempo_sobrando = fonte.render(f'Tempo restante: {int(tempo_restante)} segundos', True, (0, 0, 0))
    window.blit(tempo_sobrando, (LARGURA // 2 - tempo_sobrando.get_width() // 2, ALTURA // 2 - numero_acertos.get_height() // 2 - 60 + numero_acertos.get_height() + 20))

    mensagem_reiniciar = fonte.render("APERTE ENTER PARA VOLTAR", True, (0, 0, 0))
    window.blit(mensagem_reiniciar, (LARGURA // 2 - mensagem_reiniciar.get_width() // 2, ALTURA // 2 - numero_acertos.get_height() // 2 - 60 + numero_acertos.get_height() + 20 + tempo_sobrando.get_height() + 20))
    pygame.display.update()

tempo_reinicio = 1
proximo_reinicio = None
em_tela_inicial = True
em_game_over = False

while True:
    if em_tela_inicial:
        tela_inicial()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if botao_rect.collidepoint(mouse_pos):
                    tela_jogo()
                    em_tela_inicial = False

    elif em_game_over:
        tela_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    tela_jogo()
                    em_tela_inicial = True
                    em_game_over = False

    else:
        clock.tick(FPS)
        tempo_atual = time.time()
        tempo_restante = max(0, TEMPO_JOGO - (tempo_atual - tempo_inicio))

        if proximo_reinicio and tempo_atual >= proximo_reinicio:
            tela_jogo()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i in range(3):
                    quadrado_rect = pygame.Rect((LARGURA//2 - QUADRADO//2, ALTURA//2 - QUADRADO//2 + (i - 1) * QUADRADO), (QUADRADO, QUADRADO))
                    if quadrado_rect.collidepoint(mouse_pos) and i not in clicado:
                        clicado.append(i)
                        if valores[i] != resposta_certa:
                            VIDAS -= 1
                        else:
                            ACERTOS += 1
                        proximo_reinicio = tempo_atual + tempo_reinicio

        if VIDAS <= 0 or tempo_restante == 0:
            em_game_over = True
            tempo_termino = tempo_restante

        window.fill((255, 255, 255))
        resultado = fonte.render(f'{valores[3]}', True, (0, 0, 0))
        window.blit(resultado, (10, 10))

        vidas_texto = fonte.render(f'Vidas: {VIDAS}', True, (0, 0, 0))
        window.blit(vidas_texto, (LARGURA - 120, 10))

        desenha_quadrados(valores, clicado)

        tempo_texto = fonte.render(f'Tempo: {int(tempo_restante)}s', True, (0, 0, 0))
        window.blit(tempo_texto, (LARGURA // 2 - tempo_texto.get_width() // 2, 10))

        pygame.display.update()