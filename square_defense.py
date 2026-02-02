import pygame
import math
import random
import sys

pygame.init()

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

# IMAGEM DO MENU(imagem do menu(feita pelo artist genial e incrível Mascena))
MENU_BG = pygame.image.load("menu.png").convert()
MENU_BG = pygame.transform.scale(MENU_BG, (W, H))

MORTE_BG = pygame.image.load("death.png").convert()
MORTE_BG = pygame.transform.scale(MORTE_BG, (W, H))

TOWER_IMG = pygame.transform.scale(
    pygame.image.load("tower.png").convert_alpha(), (120, 120)
)
MAGE_IMG = pygame.transform.scale(
    pygame.image.load("mage.png").convert_alpha(), (120, 120)
)
SNIPER_IMG = pygame.transform.scale(
    pygame.image.load("sniper.png").convert_alpha(), (120, 120)
)

MENU_LARGURA = 160
MENU_X = W - MENU_LARGURA
BOTAO_TAM = 140

MENU_BOTOES = [
    pygame.Rect(MENU_X + 10, 40,  BOTAO_TAM, BOTAO_TAM),
    pygame.Rect(MENU_X + 10, 230, BOTAO_TAM, BOTAO_TAM),
    pygame.Rect(MENU_X + 10, 420, BOTAO_TAM, BOTAO_TAM)
]


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

# MENU INICIAL(menu lindo e perfeito cem porcento genial feito pelo gênio ignóbio Mascena)
def menu_inicial():
    clock = pygame.time.Clock()

    jogar_btn = pygame.Rect(W//2 - 110, 300, 220, 60)
    sair_btn  = pygame.Rect(W//2 - 110, 390, 220, 60)

    while True:
        clock.tick(FPS)
        MAPA.blit(MENU_BG, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        if jogar_btn.collidepoint(mouse_pos):
            pygame.draw.rect(MAPA, (255, 255, 255, 40), jogar_btn, 3)
        if sair_btn.collidepoint(mouse_pos):
            pygame.draw.rect(MAPA, (255, 255, 255, 40), sair_btn, 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if jogar_btn.collidepoint(event.pos):
                    return
                if sair_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# acho que a tela de morte ficou boa, a gente podia colocar música no jogo depois né
def tela_morte():
    MAPA.blit(MORTE_BG, (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)

# INIMIGOS(todos eles são betinhas buscando por redenção e sofrem com o sniper apelão)
class Enemy:
    def __init__(self, round_num):
        self.x, self.y = CAMINHO[0]
        self.velocidade = 1.5

        base_hp = 50
        multiplicador = 1.30 ** (round_num - 1)

        self.max_hp = int(base_hp * multiplicador)
        self.hp = self.max_hp

        self.caminho = 0
        self.cor = VERMELHO

    def movimento(self):
        if self.caminho >= len(CAMINHO) - 1:
            return "BASE"
        tx, ty = CAMINHO[self.caminho + 1]
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)
        if dist < self.velocidade:
            self.caminho += 1
        else:
            self.x += dx / dist * self.velocidade
            self.y += dy / dist * self.velocidade

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

# TORRES(sniper apeelão mira jamais pinada)
class Tower:
    CUSTO = 50
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.range = 120
        self.dano = 8
        self.cooldown = 30
        self.cd = 0

    def desenhar(self, tela):
        rect = TOWER_IMG.get_rect(center=(self.x, self.y))
        tela.blit(TOWER_IMG, rect)
        pygame.draw.circle(tela, (0, 0, 80), (self.x, self.y), self.range, 1)

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

    def desenhar(self, tela):
        rect = MAGE_IMG.get_rect(center=(self.x, self.y))
        tela.blit(MAGE_IMG, rect)
        pygame.draw.circle(tela, ROXO, (self.x, self.y), self.range, 1)

class SniperTower(Tower):
    CUSTO = 120
    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 300
        self.dano = 60
        self.cooldown = 90

    def desenhar(self, tela):
        rect = SNIPER_IMG.get_rect(center=(self.x, self.y))
        tela.blit(SNIPER_IMG, rect)
        pygame.draw.circle(tela, (150,150,255), (self.x, self.y), self.range, 1)

# HUD(não tenho muito o que dizer)

def desenhar_menu(tela, sel):
    pygame.draw.rect(tela,(40,40,40),(MENU_X,0,MENU_LARGURA,H))
    torres=[(TOWER_IMG,50, "Guerreiro"),(MAGE_IMG,80, "Mago"),(SNIPER_IMG,120, "Sniper")]
    for i,(img,c, nome) in enumerate(torres):
        b=MENU_BOTOES[i]
        pygame.draw.rect(tela,AMARELO if sel==i else (80,80,80),b,4 if sel==i else 2)
        tela.blit(img,img.get_rect(center=b.center))
        tela.blit(FONTE.render(f"${c}",True,BRANCO),(b.x+20,b.bottom+5))
        tela.blit(FONTE.render(f"{nome}", True, BRANCO), (b.x+60, b.bottom+5))

def menu_selecionar(pos):
    for i, botao in enumerate(MENU_BOTOES):
        if botao.collidepoint(pos):
            return i
    return None

# JOGO PRINCIPAL(bora focar mais nessa parte aqui Arthur)
def main():
    clock = pygame.time.Clock()
    inimigos, torres = [], []
    ouro, vida, round_num = 150, 10, 1
    spawn_timer = 0
    selecionado = None
    i = 6
    spawnar_inimigos = round_num * i

    while True:
        clock.tick(FPS)
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
                    if selecionado==0 and ouro>=50:
                        torres.append(Tower(mx,my)); ouro-=50
                    elif selecionado==1 and ouro>=80:
                        torres.append(MageTower(mx,my)); ouro-=80
                    elif selecionado==2 and ouro>=120:
                        torres.append(SniperTower(mx,my)); ouro-=120

        if spawnar_inimigos > 0:
            spawn_timer+=1
            if spawn_timer>=40:
                tipo = random.choice([Enemy, FastEnemy, TankEnemy])
                inimigos.append(tipo(round_num))
                spawnar_inimigos-=1; spawn_timer=0
        elif not inimigos:
            round_num += 1
            i += 1
            spawnar_inimigos = round_num * i
        for e in inimigos[:]:
            if e.movimento()=="BASE":
                vida-=1; inimigos.remove(e)
            elif e.hp<=0:
                ouro+=10; inimigos.remove(e)

        for t in torres: t.atirar(inimigos)
        for e in inimigos: e.desenhar(MAPA)
        for t in torres: t.desenhar(MAPA)

        desenhar_menu(MAPA, selecionado)
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