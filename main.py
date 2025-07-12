import pyxel

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.speed = 1.5
        self.gravity = 0.5
        self.jump_strength = -4
        self.on_ground = False


    def update(self):
        #Rörelser
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.speed
        #Hopp
        
        if pyxel.btnp(pyxel.KEY_SPACE) and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False
        #Gravitation
        self.vy += self.gravity
        self.y += self.vy
        #Markkollision
        if self.y >= 85: #kollar om spelaren fallit förbi/nuddat marknivån
            self.y = 85 #flyttar tillbaka spelaren till marknivå 
            # tänk på att spelarens position baseras på dess övre vänstra hörn(tänk 0,0)
            self.vy = 0 #stoppar spelarens vertikala rörelse
            self.on_ground = True #berättar för spelet att spelaren nu står på marken

    def draw(self):
        pyxel.rect(self.x, self.y, 8, 16, 10)
        

#Spelet
class App:
    def __init__(self):
        
        pyxel.init(160, 120, title="Springarn")
        
        self.fyrkant_x = 140 #fyrkantens x-position
        self.fyrkant_y = 92 #fyrkantens y-position
        #Spelare + startposition
        self.player = Player(50, 50)

        self.game_over = False

        pyxel.run(self.update, self.draw)

    def update(self):

        if self.game_over:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
                self.restart()
            return #hoppa över resten av update/gör så att spelet fryser
        self.player.update()

        #fyrkantens rörelser
        self.fyrkant_x = (self.fyrkant_x -2)
        if self.fyrkant_x < 40: #när denna kordinat nås gör...
            self.fyrkant_x= pyxel.width - 20 #sätt fyrkant = skärmens bredd - 20 pixlar

        #kollisionsdetektering 
        if self.check_collision(
            self.player.x, self.player.y, 8, 16,
            self.fyrkant_x, self.fyrkant_y, 8, 8
        ):
            self.game_over = True
        
    def restart(self):
        self.fyrkant_x = 140 #fyrkantens x-position
        self.player = Player(50, 50)

        self.game_over = False

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(self.fyrkant_x, self.fyrkant_y, 8, 8, 9)
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