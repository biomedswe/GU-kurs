#------------------------------------------------------
#This module contains all graphics-classes for the game
#Most classes are wrappers around model classes, e.g.
#  * GraphicGame is a wrappoer around Game
#  * GraphicPlayer is a wrapper around Player
#  * GraphicProjectile is a wrapper around Projectile
#In addition there are two UI-classes that have no
#counterparts in the model:
#  * Button
#  * InputDialog
#------------------------------------------------------



# This is the only place where graphics should be imported!
from graphics import *
from random import randint

class GraphicGame:
    def __init__(self,game):
        self.model = game
        self.win = win = GraphWin("Cannon game", 640, 480, autoflush=False)
        win.setCoords(-110,-10,110,155)
        self.model.players[0] = GraphicPlayer(self.model.players[0], self) # self på slutet skickar med GraphicGame objektet till GraphicPlayer
        self.model.players[1] = GraphicPlayer(self.model.players[1], self)
        Line(Point(-110,0),Point(110,0)).draw(win) # ritar en linje som symboliserar marken

    def getPlayers(self):
        return self.model.getPlayers()

    def getCannonSize(self):
        return self.model.getCannonSize()

    def getBallSize(self):
        return self.model.getBallSize()

    def getCurrentPlayer(self):
        return self.model.getCurrentPlayer()

    def getOtherPlayer(self):
        if self.model.currentPlayer == 0:
            return self.model.players[1]
        else:
            return self.model.players[0]

    def getCurrentPlayerNumber(self):
        return self.model.getCurrentPlayerNumber()

    def nextPlayer(self):
        if self.model.currentPlayer == 0:
            self.model.currentPlayer = 1
        else:
            self.model.currentPlayer = 0

    def setCurrentWind(self, wind):
        self.model.setCurrentWind(wind)

    def getCurrentWind(self):
        return self.model.getCurrentWind()

    def newRound(self):
        self.model.newRound()

    def getWindow(self):
        return self.win



# HINT: Don't forget to call draw() on every component you create, otherwise they will not be visible
# HINT: You need to get the Players from the Game object (the model), wrap them into GraphicPlayers and store them, and all get-methods for players (e.g. getCurrentPlayer) must return the Graphical versions

class GraphicPlayer:
    def __init__(self, player, game):
        self.player = player
        self.game = game
        print("GraphicPlayer created")
        self.proj = None # retuner ett None objekt om proj inte skapats än, används för att köra undraw() i .fire()
        # Skapar "kanonen" i form av en rektangel
        p1 = Point(player.xPos - game.getCannonSize() / 2, 0) # centrum för player (x) - halva storleken på kanonen, och y = 0
        p2 = Point(player.xPos + game.getCannonSize() / 2, game.getCannonSize()) # centrum för player (x) + halva storleken på kanonen, y = cannonSize (10)
        cannon = Rectangle(p1,p2) # skapar en rektangel (kanon), med punkterna p1 och p2
        cannon.setFill(player.getColor()) # sätter färgen till spelarens färg i modellen för player
        cannon.setOutline(player.getColor()) # Gör ytterkanten på rektangeln i samma färg som fyllnaden
        cannon.draw(game.getWindow()) # ritar kanonen genom att anropa game.getWindow() metoden
        self.scoreCounter = Text(Point(self.getX(), -5), "Score: 0") # placerar scoreCounter med texten "Score: 0"
        self.scoreCounter.draw(game.getWindow()) # ritar scoreCounter



    def fire(self, angle, velocity):
        # Fire the cannon of the underlying player object
        proj = self.player.fire(angle, velocity) # projektilmodellen som används för grafiken

        if self.proj: # om self.proj == True -> undraw(), när den är None är den false
            self.proj.undraw()

        self.proj = GraphicProjectile(proj, self.game, self.player)



        return proj

    def getAim(self):
        return self.player.getAim()

    def getColor(self):
        return self.player.getColor()

    def getX(self):
        return self.player.getX()

    def getScore(self):
        return self.player.getScore()

    def projectileDistance(self, proj):
        return self.player.projectileDistance(proj)

    def increaseScore(self):
        self.player.increaseScore()
        self.scoreCounter.setText("Score: " + str(self.getScore()))


""" A graphic wrapper around the Projectile class (adapted from ShotTracker in book)"""
class GraphicProjectile:
    def __init__(self, proj, game, player):
        self.game = game
        self.proj = proj
        self.player = player
        self.cannonball = Circle(Point(proj.getX(), proj.getY()), self.game.getBallSize())
        self.cannonball.setFill(self.player.getColor())
        self.cannonball.setOutline(self.player.getColor())
        self.cannonball.draw(game.getWindow())
    # TODO: This one also needs a constructor, and it should take a Projectile object as parameter and store it in self.proj.
    # Hint: We are also going to need access to the game window
    # Hint: There is no color attribute in the Projectile class, either it needs to be passed to the constructor here or Projectile needs to be modified.

    def update(self, dt):
        # update the projectile
        self.proj.update(dt)

        center = self.cannonball.getCenter()
        dx = self.proj.getX() - center.getX()
        dy = self.proj.getY() - center.getY()
        self.cannonball.move(dx,dy)

    def getX(self):
        return self.proj.getX()

    def getY(self):
        return self.proj.getY()

    def isMoving(self):
        return self.proj.isMoving()

    def undraw(self):
        self.cannonball.undraw()

    # TODO: There needs to be a way of undrawing the projectile.
    # HINT: All graphical components in graphics.py have undraw()-methods


""" A somewhat specific input dialog class (adapted from the book) """
class InputDialog:
    """ Takes the initial angle and velocity values, and the current wind value """
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))

        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))

        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))

        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    """ Runs a loop until the user presses either the quit or fire button """
    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    """ Returns the current values of (angle, velocity) as entered by the user"""
    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()



""" A general button class (from the book) """
class Button:

    """A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, win, center, width, height, label):
        """ Creates a rectangular button, eg:
        qb = Button(myWin, Point(30,25), 20, 10, 'Quit') """

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        "RETURNS true if button active and p is inside"
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        "RETURNS the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0
