import pygame
import math
import random
import sys

pygame.init()
pygame.mixer.init()

# CONFIGIGURAÇÕES(essa parte a gente deixa quieto porque tá funcionando bem)
W, H = 1000, 600
MAPA = pygame.display.set_mode((W, H))
pygame.display.set_caption("Square Defense")

FPS = 60
FONTE = pygame.font.SysFont("arial", 20)

# CORES(também deixa quieto)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (50, 200, 50)
VERMELHO = (200, 50, 50)
AZUL = (60, 80, 220)
ROXO = (170, 80, 255)
CINZA = (120, 120, 120)
AMARELO = (255, 220, 0)

# IMAGEM DO MENU(feita pelo artist genial e incrível Mascena)
MENU_BG = pygame.image.load("imagens/menu.png").convert()
MENU_BG = pygame.transform.scale(MENU_BG, (W, H))

MORTE_BG = pygame.image.load("imagens/death.png").convert()
MORTE_BG = pygame.transform.scale(MORTE_BG, (W, H))

TOWER_IMG = pygame.transform.scale(
    pygame.image.load("imagens/tower.png").convert_alpha(), (90, 90)
)
MAGE_IMG = pygame.transform.scale(
    pygame.image.load("imagens/mage.png").convert_alpha(), (90, 90)
)
SNIPER_IMG = pygame.transform.scale(
    pygame.image.load("imagens/sniper.png").convert_alpha(), (90, 90)
)
ICE_IMG = pygame.transform.scale(
    pygame.image.load("imagens/ice.png").convert_alpha(), (120, 120)
)
TESLA_IMG = pygame.transform.scale(
    pygame.image.load("imagens/tesla.png").convert_alpha(), (120, 120)
)
POISON_IMG = pygame.transform.scale(
    pygame.image.load("imagens/poison.png").convert_alpha(), (120, 120)
)
FIRE_IMG = pygame.transform.scale(
    pygame.image.load("imagens/fire.png").convert_alpha(), (100, 100)
)

MENU_TOWER_IMG  = pygame.transform.scale(TOWER_IMG, (60, 60))
MENU_MAGE_IMG   = pygame.transform.scale(MAGE_IMG, (60, 60))
MENU_SNIPER_IMG = pygame.transform.scale(SNIPER_IMG, (60, 60))
MENU_ICE_IMG    = pygame.transform.scale(ICE_IMG, (60, 60))
MENU_TESLA_IMG  = pygame.transform.scale(TESLA_IMG, (90, 90))
MENU_POISON_IMG = pygame.transform.scale(POISON_IMG, (60, 60))
MENU_FIRE_IMG   = pygame.transform.scale(FIRE_IMG, (60, 60))

MUSICA_MENU = "som/menu_theme_v3.wav"
MUSICA_JOGO = "som/game_theme_v2.wav"
MUSICA_MORTE = "som/death.wav"

def tocar_musica(arquivo, loop=True):
    pygame.mixer.music.load(arquivo)
    pygame.mixer.music.play(-1 if loop else 0)

MENU_LARGURA = 220
MENU_X = W - MENU_LARGURA
BOTAO_TAM = 70
ESPACO_BOTOES = 15

NUM_TORRES = 7

MENU_BOTOES = []

altura_total = NUM_TORRES * BOTAO_TAM + (NUM_TORRES - 1) * ESPACO_BOTOES
inicio_y = (H - altura_total) // 2  # CENTRALIZA VERTICALMENTE

for i in range(NUM_TORRES):
    x = MENU_X + (MENU_LARGURA - BOTAO_TAM) // 2
    y = inicio_y + i * (BOTAO_TAM + ESPACO_BOTOES)

    MENU_BOTOES.append(pygame.Rect(x, y, BOTAO_TAM, BOTAO_TAM))


# CAMINHO(tá funcionando legal)
CAMINHO = [
    (0, 300),
    (200, 300),
    (200, 150),
    (450, 150),
    (450, 450),
    (700, 450),
    (700, 250),
    (1000, 250)
]

# FUNDO DO JOGO(essa pate ate que tá boa mas se pá depois eu tento fazer um pixelart melhor )
def gerar_floresta():
    return [(random.randint(0, 900), random.randint(0, 550)) for _ in range(50)]

ARVORES = gerar_floresta()

def criar_background(tela):
    tela.fill((34, 139, 34))
    for i in range(0, 900, 20):
        for j in range(0, 600, 20):
            if (i + j) % 40 == 0:
                pygame.draw.rect(tela, (30, 120, 30), (i, j, 20, 20))
    for x, y in ARVORES:
        pygame.draw.rect(tela, (80, 40, 0), (x+10, y+20, 10, 20))
        pygame.draw.rect(tela, (10, 200, 10), (x, y, 30, 25))


FUNDO_MEL = pygame.image.load("imagens/melissa_bg.png").convert()
FUNDO_MEL = pygame.transform.scale(FUNDO_MEL, (W, H))

IMG_MEL = pygame.image.load("imagens/melissa.png").convert_alpha()
IMG_MEL = pygame.transform.scale(IMG_MEL, (150, 300))


def tela_melissa():
    clock = pygame.time.Clock()

    voltar_btn = pygame.Rect(W-160, 20, 140, 50)

    while True:
        clock.tick(FPS)
        MAPA.blit(FUNDO_MEL, (0, 0))

        # imagem central
        rect = IMG_MEL.get_rect(center=(W//2, H//2 - 50))
        MAPA.blit(IMG_MEL, rect)

        # texto
        linhas = [
            "um agradecimento especial para Melissa",
            "por fazer todos os dias do desenvolvedor",
            "desse jogo mais felizes,",
            "te amo muito Mel!"
        ]

        for i, linha in enumerate(linhas):
            txt = FONTE.render(linha, True, BRANCO)
            MAPA.blit(txt, (W//2 - txt.get_width()//2, H//2 + 140 + i*25))

        # botão voltar
        pygame.draw.rect(MAPA, (80,80,80), voltar_btn, border_radius=8)
        MAPA.blit(FONTE.render("VOLTAR", True, BRANCO),
                  (voltar_btn.x + 30, voltar_btn.y + 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if voltar_btn.collidepoint(event.pos):
                    return

        pygame.display.update()


# MENU INICIAL(menu lindo e perfeito cem porcento genial feito pelo gênio ignóbio Mascena)
def menu_inicial():
    clock = pygame.time.Clock()
    tocar_musica(MUSICA_MENU)

    jogar_btn = pygame.Rect(W//2 - 110, 290, 220, 60)
    sair_btn  = pygame.Rect(W//2 - 110, 420, 220, 60)
    coracao_btn = pygame.Rect(250, 285, 40, 40)

    while True:
        clock.tick(FPS)
        MAPA.blit(MENU_BG, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        if jogar_btn.collidepoint(mouse_pos):
            pygame.draw.rect(MAPA, (255, 255, 255, 40), jogar_btn, 3)
        if sair_btn.collidepoint(mouse_pos):
            pygame.draw.rect(MAPA, (255, 255, 255, 40), sair_btn, 3)
        if coracao_btn.collidepoint(mouse_pos):
            pygame.draw.rect(MAPA, (255, 255, 255, 40), coracao_btn, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if coracao_btn.collidepoint(event.pos):
                    tela_melissa()
                if jogar_btn.collidepoint(event.pos):
                    return
                if sair_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def tela_morte():
    tocar_musica(MUSICA_MORTE, loop=False)
    MAPA.blit(MORTE_BG, (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)

class Enemy:
    def __init__(self, round_num):
        self.poison_timer = 0
        self.poison_dano = 0
        self.slow_timer = 0
        self.slow_factor = 1
        self.x, self.y = CAMINHO[0]
        self.velocidade = 1.5

        base_hp = 50
        multiplicador = 1.30 ** (round_num - 1)

        self.max_hp = int(base_hp * multiplicador)
        self.hp = self.max_hp

        self.caminho = 0
        self.cor = VERMELHO

    def movimento(self):
        if self.poison_timer > 0:
            self.hp -= self.poison_dano
            self.poison_timer -= 1
        if self.caminho >= len(CAMINHO) - 1:
            return "BASE"

        velocidade_real = self.velocidade * self.slow_factor

        if self.slow_timer > 0:
            self.slow_timer -= 1
        else:
                self.slow_factor = 1

        tx, ty = CAMINHO[self.caminho + 1]
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)

        if dist < velocidade_real:
            self.caminho += 1
        else:
            self.x += dx / dist * velocidade_real
            self.y += dy / dist * velocidade_real

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x-10, self.y-10, 20, 20))
        pygame.draw.rect(tela, PRETO, (self.x-12, self.y-18, 25, 4))
        pygame.draw.rect(tela, VERDE, (self.x-12, self.y-18, 25*(self.hp/self.max_hp), 4))

class FastEnemy(Enemy):
    def __init__(self, round_num):
        super().__init__(round_num)
        self.velocidade = 2.0

        base_hp = 30
        multiplicador = 1.30 ** (round_num - 1)

        self.max_hp = int(base_hp * multiplicador)
        self.hp = self.max_hp
        self.cor = AMARELO

class TankEnemy(Enemy):
    def __init__(self, round_num):
        super().__init__(round_num)
        self.velocidade = 1

        base_hp = 80
        multiplicador = 1.30 ** (round_num - 1)

        self.max_hp = int(base_hp * multiplicador)
        self.hp = self.max_hp
        self.cor = CINZA

class BossEnemy(Enemy):
    def __init__(self, round_num):
        super().__init__(round_num)
        self.velocidade = 0.8
        self.cor = (255, 140, 0)  # laranja

        base_hp = 750
        multiplicador = 1.30 ** (round_num - 1)

        self.max_hp = int(base_hp * multiplicador)
        self.hp = self.max_hp

    def desenhar(self, tela):
        pygame.draw.rect(
            tela,
            self.cor,
            (self.x - 20, self.y - 20, 40, 40)
        )

        pygame.draw.rect(tela, PRETO, (self.x-22, self.y-28, 44, 6))
        pygame.draw.rect(
            tela,
            VERDE,
            (self.x-22, self.y-28, 44*(self.hp/self.max_hp), 6)
        )

class Tower:
    CUSTO = 50
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.range = 120
        self.dano = 8
        self.cooldown = 30
        self.cd = 0

    def mouse_em_cima(self, mouse_pos):
        mx, my = mouse_pos
        return math.hypot(self.x - mx, self.y - my) <= 60

    def desenhar(self, tela, mouse_pos):
        rect = TOWER_IMG.get_rect(center=(self.x + 10, self.y))
        tela.blit(TOWER_IMG, rect)

        if self.mouse_em_cima(mouse_pos):
            pygame.draw.circle(tela, (0, 0, 80), (self.x, self.y), self.range, 2)

    def atirar(self, inimigos):
        if self.cd < self.cooldown:
            self.cd += 1
            return
        for e in inimigos:
            if math.hypot(self.x-e.x, self.y-e.y) <= self.range:
                e.hp -= self.dano
                self.cd = 0
                break

class MageTower(Tower):
    CUSTO = 80
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 150
        self.dano = 20
        self.cooldown = 40

    def desenhar(self, tela, mouse_pos):
        rect = MAGE_IMG.get_rect(center=(self.x + 10, self.y))
        tela.blit(MAGE_IMG, rect)

        if self.mouse_em_cima(mouse_pos):
            pygame.draw.circle(tela, ROXO, (self.x, self.y), self.range, 2)

class SniperTower(Tower):
    CUSTO = 120
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 300
        self.dano = 60
        self.cooldown = 80

    def desenhar(self, tela, mouse_pos):
        rect = SNIPER_IMG.get_rect(center=(self.x + 10, self.y))
        tela.blit(SNIPER_IMG, rect)

        if self.mouse_em_cima(mouse_pos):
            pygame.draw.circle(tela, (150,150,255), (self.x, self.y), self.range, 2)

class IceTower(Tower):
    CUSTO = 90

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 130
        self.dano = 15
        self.cooldown = 50

    def desenhar(self, tela, mouse_pos):
        rect = ICE_IMG.get_rect(center=(self.x + 10, self.y))
        tela.blit(ICE_IMG, rect)

        if self.mouse_em_cima(mouse_pos):
            pygame.draw.circle(tela, AZUL, (self.x, self.y), self.range, 2)

    def atirar(self, inimigos):
        if self.cd < self.cooldown:
            self.cd += 1
            return

        for e in inimigos:
            if math.hypot(self.x-e.x, self.y-e.y) <= self.range:
                e.hp -= self.dano
                e.slow_factor = 0.5
                e.slow_timer = 120
                self.cd = 0
                break

class TeslaTower(Tower):
    CUSTO = 140

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 160
        self.dano = 15
        self.cooldown = 45
        self.chain = 3

    def desenhar(self, tela, mouse_pos):
        rect = TESLA_IMG.get_rect(center=(self.x + 10, self.y))
        tela.blit(TESLA_IMG, rect)

        if self.mouse_em_cima(mouse_pos):
            pygame.draw.circle(tela, (100,200,255), (self.x, self.y), self.range, 2)

    def atirar(self, inimigos):
        if self.cd < self.cooldown:
            self.cd += 1
            return

        alvos = [e for e in inimigos if math.hypot(self.x-e.x, self.y-e.y) <= self.range]

        if alvos:
            alvo_principal = alvos[0]
            atingidos = [alvo_principal]

            for e in inimigos:
                if len(atingidos) >= self.chain:
                    break
                if e not in atingidos and math.hypot(alvo_principal.x-e.x, alvo_principal.y-e.y) <= 80:
                    atingidos.append(e)

            for e in atingidos:
                e.hp -= self.dano

            self.cd = 0

class PoisonTower(Tower):
    CUSTO = 100

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 140
        self.dano = 2
        self.cooldown = 45
        self.duracao = 180

    def desenhar(self, tela, mouse_pos):
        rect = POISON_IMG.get_rect(center=(self.x + 10, self.y))
        tela.blit(POISON_IMG, rect)

        if self.mouse_em_cima(mouse_pos):
            pygame.draw.circle(tela, (0,200,0), (self.x, self.y), self.range, 2)

    def atirar(self, inimigos):
        if self.cd < self.cooldown:
            self.cd += 1
            return

        for e in inimigos:
            if math.hypot(self.x-e.x, self.y-e.y) <= self.range:
                e.poison_timer = self.duracao
                e.poison_dano = self.dano
                self.cd = 0
                break

class FireTower(Tower):
    CUSTO = 150

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 150
        self.dano = 150
        self.cooldown = 300  # 5 segundos
        self.aoe = 70        # raio da explosão

    def desenhar(self, tela, mouse_pos):
        rect = FIRE_IMG.get_rect(center=(self.x + 10, self.y))
        tela.blit(FIRE_IMG, rect)

        if self.mouse_em_cima(mouse_pos):
            pygame.draw.circle(tela, (255,100,0), (self.x, self.y), self.range, 2)

    def atirar(self, inimigos):
        if self.cd < self.cooldown:
            self.cd += 1
            return

        for alvo in inimigos:
            if math.hypot(self.x - alvo.x, self.y - alvo.y) <= self.range:

                # dano em área
                for e in inimigos:
                    if math.hypot(alvo.x - e.x, alvo.y - e.y) <= self.aoe:
                        e.hp -= self.dano

                self.cd = 0
                break
# HUD(não tenho muito o que dizer)

def desenhar_menu(tela, sel, qg, qm, qs, qi, qt, qp, qf):
    pygame.draw.rect(tela, (35,35,35), (MENU_X, 0, MENU_LARGURA, H))

    torres = [
        (MENU_TOWER_IMG, custo_progressivo(50, qg), "Guerreiro"),
        (MENU_MAGE_IMG, custo_progressivo(80, qm), "Mago"),
        (MENU_SNIPER_IMG, custo_progressivo(120, qs), "Sniper"),
        (MENU_ICE_IMG, custo_progressivo(90, qi), "Gelo"),
        (MENU_TESLA_IMG, custo_progressivo(140, qt), "Tesla"),
        (MENU_POISON_IMG, custo_progressivo(100, qp), "Veneno"),
        (MENU_FIRE_IMG, custo_progressivo(150, qf), "Fogo"),
    ]

    for i, (img, custo, nome) in enumerate(torres):
        botao = MENU_BOTOES[i]

        # Fundo do botão
        pygame.draw.rect(
            tela,
            (60,60,60),
            botao,
            border_radius=8
        )

        # Borda seleção
        pygame.draw.rect(
            tela,
            AMARELO if sel == i else (120,120,120),
            botao,
            4 if sel == i else 2,
            border_radius=8
        )

        # === SPRITE CENTRALIZADO MAIS PRA CIMA ===
        sprite_rect = img.get_rect(center=(botao.centerx, botao.centery - 10))
        tela.blit(img, sprite_rect)

        # === NOME DENTRO DO BOTÃO (parte de baixo) ===
        texto_nome = FONTE.render(nome, True, BRANCO)
        nome_rect = texto_nome.get_rect(center=(botao.centerx, botao.bottom - 28))
        tela.blit(texto_nome, nome_rect)

        # === PREÇO DENTRO DO BOTÃO (embaixo do nome) ===
        texto_preco = FONTE.render(f"${custo}", True, AMARELO)
        preco_rect = texto_preco.get_rect(center=(botao.centerx, botao.bottom - 12))
        tela.blit(texto_preco, preco_rect)

    pygame.draw.line(tela, (80,80,80), (MENU_X,0), (MENU_X,H), 3)

def menu_selecionar(pos):
    for i, botao in enumerate(MENU_BOTOES):
        if botao.collidepoint(pos):
            return i
    return None

def custo_progressivo(base, qtd):
    return int(base * (1.10 ** qtd))

# JOGO PRINCIPAL
def main():
    tocar_musica(MUSICA_JOGO)
    clock = pygame.time.Clock()
    inimigos = []
    torres = []

    qtd_guerreiro = 0
    qtd_mago = 0
    qtd_sniper = 0
    qtd_ice = 0
    qtd_tesla = 0
    qtd_poison = 0
    qtd_fire = 0

    ouro, vida, round_num = 150, 10, 1
    spawn_timer = 0
    selecionado = None
    i = 6
    spawnar_inimigos = round_num * i
    boss_fila = 0

    if round_num % 5 == 0:
        boss_fila = 2 ** ((round_num // 5) - 1)

    while True:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        spawn_delay_normal = max(12, 40 - round_num * 1.5)
        spawn_delay_boss = max(40, 90 - round_num * 2)

        criar_background(MAPA)
        pygame.draw.lines(MAPA,(200,180,100),False,CAMINHO,10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                if mx>=MENU_X:
                    selecionado = menu_selecionar((mx,my))
                else:
                    if selecionado == 0:
                        custo = custo_progressivo(50, qtd_guerreiro)
                        if ouro >= custo:
                            torres.append(Tower(mx, my))
                            ouro -= custo
                            qtd_guerreiro += 1

                    elif selecionado == 1:
                        custo = custo_progressivo(80, qtd_mago)
                        if ouro >= custo:
                            torres.append(MageTower(mx, my))
                            ouro -= custo
                            qtd_mago += 1

                    elif selecionado == 2:
                        custo = custo_progressivo(120, qtd_sniper)
                        if ouro >= custo:
                            torres.append(SniperTower(mx, my))
                            ouro -= custo
                            qtd_sniper += 1

                    elif selecionado == 3:
                        custo = custo_progressivo(90, qtd_ice)
                        if ouro >= custo:
                            torres.append(IceTower(mx, my))
                            ouro -= custo
                            qtd_ice += 1

                    elif selecionado == 4:
                        custo = custo_progressivo(140, qtd_tesla)
                        if ouro >= custo:
                            torres.append(TeslaTower(mx, my))
                            ouro -= custo
                            qtd_tesla += 1

                    elif selecionado == 5:
                        custo = custo_progressivo(100, qtd_poison)
                        if ouro >= custo:
                            torres.append(PoisonTower(mx, my))
                            ouro -= custo
                            qtd_poison += 1

                    elif selecionado == 6:
                        custo = custo_progressivo(150, qtd_fire)
                        if ouro >= custo:
                            torres.append(FireTower(mx, my))
                            ouro -= custo
                            qtd_fire += 1

        if boss_fila > 0:
            spawn_timer += 1
            if spawn_timer >= spawn_delay_boss:
                inimigos.append(BossEnemy(round_num))
                boss_fila -= 1
                spawn_timer = 0

        elif spawnar_inimigos > 0:
            spawn_timer += 1
            if spawn_timer >= spawn_delay_normal:
                tipo = random.choice([Enemy, FastEnemy, TankEnemy])
                inimigos.append(tipo(round_num))
                spawnar_inimigos -= 1
                spawn_timer = 0
        elif not inimigos:
            round_num += 1
            i += 1
            spawnar_inimigos = round_num * i
            boss_fila = 0

            if round_num % 5 == 0:
                boss_fila = 2 ** ((round_num // 5) - 1)
        for e in inimigos[:]:
            if e.movimento() == "BASE":
                if isinstance(e, FastEnemy):
                    vida -= 1
                elif isinstance(e, BossEnemy):
                    vida -= 5
                else:
                    vida -= 1
                inimigos.remove(e)
            elif e.hp <= 0:
                reducao = (round_num // 5) * 2
                ganho = max(2, 14 - reducao)
                ouro += ganho
                inimigos.remove(e)

        for t in torres: t.atirar(inimigos)
        for e in inimigos: e.desenhar(MAPA)
        for t in torres:
            t.desenhar(MAPA, mouse_pos)

        desenhar_menu(MAPA, selecionado, qtd_guerreiro, qtd_mago, qtd_sniper, qtd_ice, qtd_tesla, qtd_poison, qtd_fire)
        MAPA.blit(FONTE.render(f"$ {ouro}   vida: {vida}   Round {round_num}",True,BRANCO),(10,10))
        pygame.display.update()

        if vida <= 0:
            tela_morte()
            return 

# EXECUÇÃO(fruto lindo do nosso trabalho)
if __name__ == "__main__":
    while True:
        menu_inicial()
        main()