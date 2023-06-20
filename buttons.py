from graphics import *

win = GraphWin("Oden kykly", 1000, 675)


class button:
    def __init__(self, p1, p2, text, win):
        self.p1 = p1
        self.p2 = p2
        self.text = text
        self.win = win
        buttoninstance = Rectangle(self.p1, self.p2)
        self.buttoninstance = buttoninstance

    def draw(self):
        self.buttoninstance.draw(self.win)
        self.buttoninstance.setFill(color_rgb(255, 224, 249))
        self.buttoninstance.setOutline("white")
        self.textinstance = Text(
            Point((self.p2.x - self.p1.x) / 2 + self.p1.x,
                  (self.p2.y - self.p1.y) / 2 + self.p1.y), self.text)
        self.textinstance.draw(self.win)

    def undraw(self):
        print("undraw button")
        self.buttoninstance.undraw()
        self.textinstance.setText("")


button1 = button(Point(525, 50), Point(725, 200), "bottoms", win)
button2 = button(Point(775, 50), Point(975, 200), "tops", win)
button4 = button(Point(775, 250), Point(975, 400), "wheee", win)
button5 = button(Point(525, 450), Point(725, 600), "wheee", win)
button6 = button(Point(775, 450), Point(975, 600), "done", win)
backbutton = button(Point(10, 10), Point(150, 75), "done", win)


def create_start():
    button1.draw()
    button2.draw()
    button6.draw()


def set_up_closet():
    button1.undraw()
    button2.undraw()
    button6.undraw()
    backbutton.draw()
