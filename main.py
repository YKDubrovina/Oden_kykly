# Одень куклу

from graphics import *
from buttons import *

start_up = Image(Point(510, 300), "img/startup1.gif")
start_up.draw(win)
model = Image(Point(210, 400), "img/model.png")
model.draw(win)


class Finished_cat:
    def __init__(self, x, y):
        self.model = Image(Point(x, y), "img/model.png")
        # model.draw(win)
        self.top = None
        self.bottom = None

    def store_top(self, fname, x, y):
        self.top = Image(Point(x, y), fname)

    def store_bottom(self, fname, x, y):
        self.bottom = Image(Point(x, y), fname)

    def draw(self):

        self.model.draw(win)

        if self.top != None:
            self.top.draw(win)
        if self.bottom != None:
            self.bottom.draw(win)


random_variable = Finished_cat(600, 400)

current_top = []
current_skirt = ''

current_top = ''


outfit = []
clothes = []


class Clothes:
    def __init__(self, win, p1, p2, image):
        self.p1 = p1
        self.p2 = p2
        self.win = win
        self.image = image
        clothesinstance = Image(Point(self.p1, self.p2), self.image)
        self.clothesinstance = clothesinstance

    def draw(self):
        self.clothesinstance.draw(self.win)

    def undraw(self):
        self.clothesinstance.undraw()

    def append(self):
        clothes.append(self.clothesinstance)
        return clothes


    def get_left_side(self):
        self.width = self.clothesinstance.getWidth()
        self.center_prev = self.clothesinstance.getAnchor()
        left_side = int(self.center_prev.getX()) - self.width
        return left_side

    def get_right_side(self):
        self.width = self.clothesinstance.getWidth()
        self.center_prev = self.clothesinstance.getAnchor()
        right_side = int(self.center_prev.getX()) + self.width
        return right_side

    def get_bottom(self):
        self.height = self.clothesinstance.getHeight()
        self.center_prev = self.clothesinstance.getAnchor()
        bottom = int(self.center_prev.getY()) - self.height
        return bottom

    def get_top(self):
        self.height = self.clothesinstance.getHeight()
        self.center_prev = self.clothesinstance.getAnchor()
        top = int(self.center_prev.getY()) + self.height
        return top


def main():
    in_closet = "false"
    while True:
        while in_closet == "false":
            create_start()
            print("at menu")
            mouseclick = win.getMouse()
            print("hey", mouseclick.x, mouseclick.y)

            if (525 < mouseclick.x < 725) and (50 < mouseclick.y < 200):
                print("set up closet")

                set_up_closet()

                pink_skirt = Clothes(win, 600, 200, "img/pink_skirt.png")
                pink_skirt.draw()
                purple_skirt = Clothes(win, 900, 200, "img/purple_skirt.png")
                purple_skirt.draw()
                current_skirt = 'purple skirt'

                purple_right = purple_skirt.get_right_side()
                purple_left = purple_skirt.get_left_side()
                purple_bottom = purple_skirt.get_bottom()
                purple_top = purple_skirt.get_top()

                pink_right = pink_skirt.get_right_side()
                pink_left = pink_skirt.get_left_side()
                pink_bottom = pink_skirt.get_bottom()
                pink_top = pink_skirt.get_top()


                in_closet = "bottoms"
                print("in closet:", in_closet)

            elif 775 < mouseclick.x < 975 and 50 < mouseclick.y < 200:
                print("in the next loop")
                set_up_closet()

                striped_shirt = Clothes(win, 640, 250, "img/striped_shirt.png")
                striped_shirt.draw()

                sweater = Clothes(win, 880, 250, "img/sweater.png")
                sweater.draw()

                in_closet = "tops"
                print("in closet:", in_closet)

            # the other buttons will lead to other categories of clothes
            elif 525 < mouseclick.x < 725 and 250 < mouseclick.y < 400:
                set_up_closet()
                print("in hats")
                crown = Clothes(win, 600, 200, "img/crown.png")
                crown.draw()
                crown_right = crown.get_right_side()
                crown_left = crown.get_left_side()
                crown_bottom = crown.get_bottom()
                crown_top = crown.get_top()

                in_closet = "hats"

            elif 775 < mouseclick.x < 975 and 250 < mouseclick.y < 400:
                set_up_closet()

                in_closet = "weeee"

            elif 525 < mouseclick.x < 725 and 450 < mouseclick.y < 600:
                set_up_closet()

                in_closet = "weeee"

            elif 775 < mouseclick.x < 975 and 450 < mouseclick.y < 600:

                in_closet = "done"



        if in_closet == "done":

            start_up.undraw()

            print("In done")
            button1.undraw()
            button2.undraw()
            button3.undraw()
            button6.undraw()

            model.undraw()

            if random_variable.top == 'striped_shirt':
                print("take off striped shirt")
                striped_shirt_on_cat.undraw()

            print("undraws")




        while in_closet == "bottoms":
            print("in bottoms")
            mouseclick = win.getMouse()


            if (int(purple_left)) < mouseclick.x < (int(purple_right)) and (
                    int(purple_bottom)) < mouseclick.y < (int(purple_top)):
                print("put on purple skirt")
                current_skirt = "purple skirt"
                random_variable.store_bottom("img/purple_skirt.png", 625, 500)



                purple_skirt.undraw()
                purple_skirt_on_cat = Image(Point(237, 490),
                                            "img/purple_skirt.png")

                purple_skirt_on_cat.draw(win)

            if (int(pink_left)) < mouseclick.x < (int(pink_right)) and (
                    int(pink_bottom)) < mouseclick.y < (int(pink_top)):
                print("put on pink skirt")
                current_skirt = "pink skirt"
                random_variable.store_bottom("img/pink_skirt.png", 625, 500)
                pink_skirt.undraw()

                pink_skirt_on_cat = Image(Point(237, 490),
                                          "img/pink_skirt.png")
                pink_skirt_on_cat.draw(win)

            if (187 < mouseclick.x < 287) and (440 < mouseclick.y < 540):
                print("clicked to take off skirt")
                random_variable.store_bottom("img/empty.png", 0, 1)
                print(random_variable.bottom)
                if current_skirt == "pink skirt":
                    print("current skirt is pink")
                    pink_skirt_on_cat.undraw()
                    pink_skirt = Clothes(win, 600, 200, "img/pink_skirt.png")
                    print("took of pink skirt, redrawing it now")
                    pink_skirt.draw()
                    print("drawing skirt again")
                elif current_skirt == "purple skirt":
                    print("current skirt is purple")
                    purple_skirt_on_cat.undraw()
                    purple_skirt = Clothes(win, 900, 200, "img/purple_skirt.png")
                    purple_skirt.draw()
                    print("drew")



            if 10 < mouseclick.x < 150 and 10 < mouseclick.y < 75:
                print("back")
                purple_skirt.undraw()
                pink_skirt.undraw()
                backbutton.undraw()
                in_closet = "false"

        while in_closet == "tops":
            print("in tops")
            mouseclick = win.getMouse()


            striped_right = striped_shirt.get_right_side()
            striped_left = striped_shirt.get_left_side()
            striped_bottom = striped_shirt.get_bottom()
            striped_top = striped_shirt.get_top()

            sweater_right = sweater.get_right_side()
            sweater_left = sweater.get_left_side()
            sweater_bottom = sweater.get_bottom()
            sweater_top = sweater.get_top()

            if (int(striped_left)) < mouseclick.x < (int(striped_right)) and (int(striped_bottom)) < mouseclick.y < (
                    int(striped_top)):

                current_top = "striped shirt"

                random_variable.store_top("img/striped_shirt.png", 625, 420)
                striped_shirt.undraw()
                striped_shirt_on_cat = Image(Point(232, 434),
                                             "img/striped_shirt.png")
                striped_shirt_on_cat.draw(win)
            if (int(sweater_left)) < mouseclick.x < (int(sweater_right)) and (int(sweater_bottom)) < mouseclick.y < (
                    int(sweater_top)):

                current_top = "striped shirt"

                sweater.undraw()
                sweater_on_cat = Image(Point(232, 424),
                                       "img/sweater.png")
                sweater_on_cat.draw(win)

            if (187 < mouseclick.x < 287) and (237 < mouseclick.y < 425):

                if current_top == "striped shirt":

                    striped_shirt_on_cat.undraw()
                    striped_shirt = Clothes(win, 600, 200, "img/striped_shirt.png")

                    striped_shirt.draw()


            if 10 < mouseclick.x < 150 and 10 < mouseclick.y < 75:
                print("back")
                backbutton.undraw()
                striped_shirt.undraw()


                in_closet = "false"

        while in_closet == "acessories":
            pass





            if (217 < mouseclick.x < 300) and (160 < mouseclick.y < 300):
                print("clicked to take off crown")

                if random_variable.hat == (Image(Point(625.0, 220.0), 172, 100)):
                    crown_on_cat.undraw()
                    crown.draw()




            if 10 < mouseclick.x < 150 and 10 < mouseclick.y < 75:
                print("back")
                backbutton.undraw()
                in_closet = "false"




main()
