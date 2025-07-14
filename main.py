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
        

#Spelet
class App:
    def __init__(self):
        
        pyxel.init(160, 120, title="Run fo yo life")

        #Tidtagning variabler
        self.tidtagning = pyxel.frame_count #frame_count är en funktion som räknar fps. I pyxel 30fps/s
        self.sekund = 0
        self.phs = 0 #placeholder sekund
        self.minut = 0
        
        #hinder
        self.fyrkant_x = 170 #fyrkantens x-position
        self.fyrkant_y = 92 #fyrkantens y-position
        self.redsquare_x = 190
        self.redsquare_y = 86
        self.longsquare_x = 256
        self.longsquare_y = 92
        
        #markens rörelse
        self.mark_x = 160
        self.mark2_x = 20
        self.mark3_x = 70

        #Spelare + startposition
        self.start_x = 50
        self.start_y = -10
        self.player = Player(self.start_x, self.start_y)

        self.game_over = False

        pyxel.run(self.update, self.draw)

    def update(self):

        #Tidtagning logik
        self.sekund = (pyxel.frame_count - self.tidtagning) // 30 #30fps/30 = 1 sek
        if self.sekund == 10:
            self.phs = ""
        if self.sekund == 60:
            self.tidtagning = pyxel.frame_count
            self.minut = self.minut + 1
        if self.sekund == 0:
            self.phs = 0

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.restart()
            return #hoppa över resten av update/gör så att spelet fryser
        self.player.update()

        #fiende rörelser
        self.fyrkant_x = (self.fyrkant_x -2)
        if self.fyrkant_x < -10: #när denna kordinat nås...
            self.fyrkant_x= pyxel.width + 10 #sätt fyrkant = skärmens bredd + 10 pixlar
        self.redsquare_x = (self.redsquare_x -2)
        if self.redsquare_x < -30:
            self.redsquare_x= pyxel.width + 80
        self.longsquare_x = (self.longsquare_x -2)
        if self.longsquare_x < -90:
            self.longsquare_x= pyxel.width + 240

        #kollisionsdetektering 
        if self.check_collision(
            self.player.x, self.player.y, 8, 8, #hitbox spelare
            self.fyrkant_x, self.fyrkant_y, 8, 8
        ):
            self.game_over = True
        if self.check_collision(
            self.player.x, self.player.y, 8, 8,
            self.redsquare_x, self.redsquare_y, 8, 8
        ):
            self.game_over = True
        if self.check_collision(
            self.player.x, self.player.y, 8, 8,
            self.longsquare_x, self.longsquare_y, 8, 8
        ):
            self.game_over = True

        #markens rörelse
        self.mark_x = (self.mark_x - 2) % pyxel.width
        self.mark2_x = (self.mark2_x - 2)
        if self.mark2_x < -10:
            self.mark2_x = pyxel.width + 165
        self.mark3_x = (self.mark3_x - 2)
        if self.mark3_x < -10:
            self.mark3_x = pyxel.width + 170
        
    def restart(self):
        self.fyrkant_x = 170 #fyrkantens x-position
        self.redsquare_x = 190
        self.longsquare_x = 256
        self.player = Player(self.start_x, self.start_y)

        self.game_over = False

    def draw(self):
        pyxel.cls(0)

        #Tidtagning utskrift
        pyxel.text(5, 5, f"Time: {self.minut}:{self.phs}{self.sekund}", 7)

        #fiender
        pyxel.rect(self.fyrkant_x, self.fyrkant_y, 8, 8, 9)
        pyxel.rect(self.redsquare_x, self.redsquare_y, 8, 14, 2)
        pyxel.rect(self.longsquare_x, self.longsquare_y, 8, 8, 7)

        #marken
        pyxel.rect(self.mark_x, 105, 2, 2, 3)
        pyxel.rect(self.mark2_x, 110, 2, 2, 3)
        pyxel.rect(self.mark3_x, 112, 2, 2, 3)
        pyxel.text(20, 20, "Run fo yo life", 10)
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