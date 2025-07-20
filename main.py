import pyxel

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.speed = 1.5
        self.gravity = 0.5
        self.jump_strength = -5
        self.on_ground = False


    def update(self):
        #Rörelser
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        
        #Hopp mekanik
        if self.on_ground: 
            self.vy = self.jump_strength
            self.on_ground = False
        
        #Gravitation
        self.vy += self.gravity
        self.y += self.vy

        #Markkollision
        if self.y >= 92: #kollar om spelaren fallit förbi/nuddat marknivån
            self.y = 92 #flyttar tillbaka spelaren till marknivå 
            # tänk på att spelarens position baseras på dess övre vänstra hörn(tänk 0,0)
            self.vy = 0 #stoppar spelarens vertikala rörelse
            self.on_ground = True #berättar för spelet att spelaren nu står på marken
        
        #Väggkollision 
        if self.x < 0: #kollar om spelaren passerar x=0
            self.x = 0 #flyttar tillbaka spelaren till x=0
        if self.x > 152:
            self.x = 152
            # tänk på att spelarens position baseras på dess övre vänstra hörn(tänk 0,0)


    def draw(self):
        pyxel.rect(self.x, self.y, 8, 8, 10)
        

class Hinder:
    def __init__(self, x, y, w, h, speed, rs, end, color, tidsstyrd = False):
        self.x = x
        self.startx = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.rs = rs #resetvärde pyxelwidth + x
        self.end = end
        self.color = color
        self.tidsstyrd = tidsstyrd #vilka fiender som spawnar senare

    def update(self):
        self.x -= self.speed #indikerar att fiender rör sig från höger till vänster
        if self.x < self.end:
            self.x = pyxel.width + self.rs
            #pyxel.width + pyxel.rndi(170,190) #kodrad med randint
            #self.x = self.startx

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.color)

    def reset(self):
        self.x = self.startx

class App:
    def __init__(self):
        
        pyxel.init(160, 120, title="Run fo yo life")

        #Tidtagning variabler
        self.tidtagning = pyxel.frame_count #frame_count är en funktion som räknar fps. I pyxel 30fps/s
        self.sekund = 0
        self.phs = 0 #placeholder sekund
        self.minut = 0
        
        
        #oop fiendelista
        self.allahinder = [
            #Hinder(x, y, w, h, speed, resetvärde, end-värde, color, tidsstyrd)
            Hinder(170, 92, 8, 8, 2, 10, -10, 9), #den gamla fyrkant
            Hinder(190, 86, 8, 14, 2, 80, -30, 2), #redsquare
            Hinder(256, 92, 8, 8, 2, 240, -90, 1), #longsquare
        ]
        #tidsaktiverade hiender
        self.hinder_aktiverad = False

        #markens rörelse
        self.mark_x = 160
        self.mark2_x = 20
        self.mark3_x = 70

        #Spelare + startposition
        self.start_x = 10
        self.start_y = -10
        self.player = Player(self.start_x, self.start_y)

        self.game_over = False

        pyxel.run(self.update, self.draw)

    def update(self):

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.restart()
            return #hoppa över resten av update/gör så att spelet fryser
        self.player.update()

        #Tidtagning logik
        self.sekund = (pyxel.frame_count - self.tidtagning) // 30 #30fps/30 = 1 sek
        if self.sekund == 10:
            self.phs = ""
        if self.sekund == 60:
            self.tidtagning = pyxel.frame_count
            self.minut = self.minut + 1
        if self.sekund == 0:
            self.phs = 0
        
        #OOP Hinder kollision
        for hinder in self.allahinder:
            hinder.update()
            if self.check_collision(self.player.x, self.player.y, 8, 8, 
                                hinder.x, hinder.y, hinder.w, hinder.h):
                self.game_over = True

        #tidsaktiverade hinder
        if not self.hinder_aktiverad and self.sekund >= 30:
            self.allahinder.append(Hinder(150, 72, 4, 4, 3, 200, -150, 7, tidsstyrd = True)) #flysquare
            self.hinder_aktiverad = True

        #markens rörelse
        self.mark_x = (self.mark_x - 2) % pyxel.width
        self.mark2_x = (self.mark2_x - 2)
        if self.mark2_x < -10:
            self.mark2_x = pyxel.width + 165
        self.mark3_x = (self.mark3_x - 2)
        if self.mark3_x < -10:
            self.mark3_x = pyxel.width + 170
        
    def restart(self):
        self.hinder_aktiverad = False
        self.tidtagning = pyxel.frame_count #behövs för att starta om tidtagningen

        #skapar ny lista allahinder och tar bort alla tidsaktiverade hinder från den tidigare listan men behåller de fasta
        self.allahinder = [h for h in self.allahinder if not h.tidsstyrd] 
        for hinder in self.allahinder:
            hinder.reset()
        self.player = Player(self.start_x, self.start_y)
        self.game_over = False

    def draw(self):
        pyxel.cls(0)

        #Tidtagning utskrift
        pyxel.text(5, 5, f"Time: {self.minut}:{self.phs}{self.sekund}", 7)

        #OOP Hinder
        for hinder in self.allahinder:
            hinder.draw()

        #marken
        pyxel.rect(self.mark_x, 105, 2, 2, 3)
        pyxel.rect(self.mark2_x, 110, 2, 2, 3)
        pyxel.rect(self.mark3_x, 112, 2, 2, 3)

        pyxel.text(20, 20, "Run fo yo life", 10)
        pyxel.circb(140, 10, 50, 7)
        self.player.draw()

        #world
        pyxel.line(0, 100, 160, 100, 3) #marken

        #kollision
        if self.game_over:
            pyxel.text(50, 60, "Game over", pyxel.frame_count % 16)
    
    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        #1 representerar spelare, 2 representerar objekt/fiende
        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )

App()