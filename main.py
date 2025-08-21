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
        self.alive = True


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
        #pyxel.rect(self.x, self.y, 8, 8, 10)
        if self.alive == False:
            pyxel.blt(self.x, self.y, 0, 32, 8, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 32 if self.y > 80 else 24, 0, 8, 8, 0) #sämsta animationskoden ever?
        
    def get_hitbox(self):
        # Göt hitbox 2px mindre på varje sida
        return self.x + 2, self.y + 2, 4, 4
        # +2 flytter startpunkten för hitboxen enligt koordinatsystemet
        # 4,4 anger hitboxens storlek

class Hinder:
    def __init__(self, x, y, w, h, speed, rs, end, u, v, tidsstyrd = False):
        self.x = x
        self.startx = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.rs = rs #resetvärde pyxelwidth + x
        self.end = end
        self.u = u
        self.v = v
        self.tidsstyrd = tidsstyrd #vilka fiender som spawnar senare

        #animation
        self.frame = 0
        self.tick = 0
        self.frames = 4 #hur många frames animationen ska ha
        self.frame_w = self.w #vilken startframe animationen ska ha, har satt samma som statiska hinder för att underlätta
        self.frame_h = self.h
    

    def update(self):
        self.x -= self.speed #indikerar att fiender rör sig från höger till vänster
        if self.x < self.end:
            self.x = pyxel.width + self.rs
            #pyxel.width + pyxel.rndi(170,190) #kodrad med randint
            #self.x = self.startx

        #animation för tidsstyrda hinder
        if self.tidsstyrd:
            self.tick += 1
            if self.tick % 4 == 0: # byt frame var 8:e update
                self.frame = (self.frame + 1) % self.frames #byter till nästa frame

    def draw(self):
        if self.tidsstyrd:
            pyxel.blt(
                self.x,
                self.y,
                0,
                self.u + self.frame * self.frame_w,
                self.v,
                self.frame_w,
                self.frame_h,
                0
            )
        else:
            #pyxel.rect(self.x, self.y, self.w, self.h, self.color)
            pyxel.blt(self.x, self.y, 0, self.u, self.v, self.w, self.h, colkey=0)

    def reset(self):
        self.x = self.startx
        self.frame = 0
        self.tick = 0

class App:
    def __init__(self):

        pyxel.init(160, 120, title="Bouncy Cat", display_scale=4)
        pyxel.load("game.pyxres")

        #Tidtagning variabler
        self.tidtagning = pyxel.frame_count #frame_count är en funktion som räknar fps. I pyxel 30fps/s
        self.sekund = 0
        self.phs = 0 #placeholder sekund
        self.minut = 0
        #Rekord
        self.rekords = 0
        self.rekordm = 0
        self.rekphs = 0

        #rörlig bakgrund, se marken i update och draw
        self.scroll_offset = 0
        self.scroll_speed = 2
        
        
        #oop fiendelista - i listor hamnar föremålen tvärtom, alltså blir soptunnan längst bak och stoppskylt längst fram på skärmen
        self.allahinder = [
            #Hinder(x, y, w, h, speed, resetvärde, end-värde, u, v, tidsstyrd) 
            Hinder(256, 92, 8, 8, 2, 240, -90, 0, 8), #soptunna
            Hinder(170, 92, 6, 8, 2, 10, -10, 9, 0), #brandpost
            Hinder(190, 86, 8, 14, 2, 80, -30, 16, 0), #stoppskylt
        ]
        #tidsaktiverade hiender
        self.hinder_aktiverad = False #krävs för att spriten inte ska målas på varenda frame hela tiden
        self.hinder2_aktiverad = False
        self.hinder_paus = True

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
        if self.hinder_paus and self.sekund > 3: #fördröjer fiender/hinder med 3 sekunder första minuten
            self.hinder_paus = False
        if not self.hinder_paus: #om 1 minut är passerad körs spelet som vanligt utan 3sek fördröjning
            px, py, pw, ph = self.player.get_hitbox()

            for hinder in self.allahinder:
                hinder.update()
                if self.check_collision(px, py, pw, ph, 
                                    hinder.x, hinder.y, hinder.w, hinder.h):
                    self.player.alive = False
                    self.game_over = True

        #tidsaktiverade hinder
        #Hinder(x, y, w, h, speed, resetvärde, end-värde, u, v, tidsstyrd)
        if not self.hinder2_aktiverad and self.sekund == 34:
            self.allahinder.append(Hinder(160, 72, 8, 7, 3, 300, -250, 120, 0, tidsstyrd = True)) #fågel resetvärdet kan behöva tweakas
            self.hinder2_aktiverad = True

        if not self.hinder_aktiverad and self.minut == 1 and self.sekund >= 5:
            self.allahinder.append(Hinder(160, 87, 16, 13, 4, 500, -500, 56, 3, tidsstyrd = True)) #hund
            self.hinder_aktiverad = True

        #marken(forloop i draw)
        self.scroll_offset += self.scroll_speed
        if self.scroll_offset >= 160:
            self.scroll_offset -= 160
        #markens rörelse
        self.mark_x = (self.mark_x - 2) % pyxel.width
        self.mark2_x = (self.mark2_x - 2)
        if self.mark2_x < -10:
            self.mark2_x = pyxel.width + 165
        self.mark3_x = (self.mark3_x - 2)
        if self.mark3_x < -10:
            self.mark3_x = pyxel.width + 170

    def restart(self):
        self.save_highscore()
        self.hinder_aktiverad = False
        self.hinder2_aktiverad = False
        self.hinder_paus = True #säkerställer 3-sekundsfrist även efter game over
        self.tidtagning = pyxel.frame_count #behövs för att starta om tidtagningen

        #skapar ny lista allahinder och tar bort alla tidsaktiverade hinder från den tidigare listan men behåller de fasta
        self.allahinder = [h for h in self.allahinder if not h.tidsstyrd] 
        for hinder in self.allahinder:
            hinder.reset()
        self.player = Player(self.start_x, self.start_y)
        self.game_over = False
        self.player.alive = True #Undersök denna
        self.minut = 0 #manuell nollställning av minuträknare

    def save_highscore(self):
        if self.minut == self.rekordm:
            if self.sekund > self.rekords:
                self.rekords = self.sekund
                self.rekphs = 0
        if self.minut > self.rekordm:
            self.rekordm = self.minut
            self.rekords = self.sekund
            self.rekphs = 0
        if self.rekords >= 10:
            self.rekphs = ""

    def draw(self):
        pyxel.cls(6)

        # Hus
        pyxel.blt(20, 36, 0, 0, 88, 115, 32, 0)

        #mur
        for i in range(2):
            x = i * 160 - int(self.scroll_offset)
            pyxel.blt(x, 60, 0, 0, 40, 160, 40, colkey=0)
        

        #Tidtagning utskrift
        pyxel.text(5, 5, f"Time: {self.minut}:{self.phs}{self.sekund}", 7)

        #High score
        pyxel.text(110, 5, f"Record: {self.rekordm}:{self.rekphs}{self.rekords}", 7)

        #OOP Hinder
        for hinder in self.allahinder:
            hinder.draw()

        #marken
        pyxel.rect(self.mark_x, 105, 2, 2, 3)
        pyxel.rect(self.mark2_x, 110, 2, 2, 3)
        pyxel.rect(self.mark3_x, 112, 2, 2, 3)

        pyxel.text(20, 20, "Bouncy Cat", 10)

        pyxel.circb(140, 10, 50, 7)

        self.player.draw()

        #marken(logik i update)
        for i in range(2):
            x = i * 160 - int(self.scroll_offset)
            pyxel.blt(x, 100, 0, 0, 16, 160, 20, colkey=2)

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