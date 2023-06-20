__version__ = "5.0"

import os
import time
import tkinter as tk



##########################################################################
# Исключения модуля

class GraphicsError(Exception):
    """Общий класс ошибок для исключений графического модуля."""
    pass


OBJ_ALREADY_DRAWN = "Object currently drawn"
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"

##########################################################################
# глобальные переменные и функции

_root = tk.Tk()
_root.withdraw()

_update_lasttime = time.time()


def update(rate=None):
    global _update_lasttime
    if rate:
        now = time.time()
        pauseLength = 1 / rate - (now - _update_lasttime)
        if pauseLength > 0:
            time.sleep(pauseLength)
            _update_lasttime = now + pauseLength
        else:
            _update_lasttime = now

    _root.update()


############################################################################

class GraphWin(tk.Canvas):
    """GraphWin - это окно верхнего уровня для отображения графики."""

    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=True):
        assert type(title) == type(""), "Title must be a string"
        master = tk.Toplevel(_root)
        master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Canvas.__init__(self, master, width=width, height=height,
                           highlightthickness=0, bd=0)
        self.master.title(title)
        self.pack()
        master.resizable(0, 0)
        self.foreground = "black"
        self.items = []
        self.mouseX = None
        self.mouseY = None
        self.bind("<Button-1>", self._onClick)
        self.bind_all("<Key>", self._onKey)
        self.height = int(height)
        self.width = int(width)
        self.autoflush = autoflush
        self._mouseCallback = None
        self.trans = None
        self.closed = False
        master.lift()
        self.lastKey = ""
        if autoflush: _root.update()

    def __repr__(self):
        if self.isClosed():
            return "<Closed GraphWin>"
        else:
            return "GraphWin('{}', {}, {})".format(self.master.title(),
                                                   self.getWidth(),
                                                   self.getHeight())

    def __str__(self):
        return repr(self)

    def __checkOpen(self):
        if self.closed:
            raise GraphicsError("window is closed")

    def _onKey(self, evnt):
        self.lastKey = evnt.keysym

    def setBackground(self, color):
        """Установите цвет фона окна"""
        self.__checkOpen()
        self.config(bg=color)
        self.__autoflush()

    def setCoords(self, x1, y1, x2, y2):
        """Установите координаты окна для запуска от (x1,y1) в левом
    нижнем углу до (x2,y2) в правом верхнем углу."""
        self.trans = Transform(self.width, self.height, x1, y1, x2, y2)
        self.redraw()

    def close(self):
        """Закройте окно"""

        if self.closed: return
        self.closed = True
        self.master.destroy()
        self.__autoflush()

    def isClosed(self):
        return self.closed

    def isOpen(self):
        return not self.closed

    def __autoflush(self):
        if self.autoflush:
            _root.update()

    def plot(self, x, y, color="black"):
        """Установите пиксель (x,y) заданного цвета"""
        self.__checkOpen()
        xs, ys = self.toScreen(x, y)
        self.create_line(xs, ys, xs + 1, ys, fill=color)
        self.__autoflush()

    def plotPixel(self, x, y, color="black"):
        """Установите пиксель в исходном виде (независимо от координат окна) Пиксель
        (x,y) для раскрашивания"""
        self.__checkOpen()
        self.create_line(x, y, x + 1, y, fill=color)
        self.__autoflush()

    def flush(self):
        """Обновите чертеж в окне"""
        self.__checkOpen()
        self.update_idletasks()

    def getMouse(self):
        """Дождитесь щелчка мыши и верните точечный объект, представляющий
        щелчок"""
        self.update()  # удалить все предыдущие клики
        self.mouseX = None
        self.mouseY = None
        while self.mouseX == None or self.mouseY == None:
            self.update()
            if self.isClosed(): raise GraphicsError("getMouse in closed window")
            time.sleep(.1)  # откажитесь от нити
        x, y = self.toWorld(self.mouseX, self.mouseY)
        self.mouseX = None
        self.mouseY = None
        return Point(x, y)

    def checkMouse(self):
        """Возвращает последний щелчок мыши или нет, если мышь
    не была нажата с момента последнего вызова"""
        if self.isClosed():
            raise GraphicsError("checkMouse in closed window")
        self.update()
        if self.mouseX != None and self.mouseY != None:
            x, y = self.toWorld(self.mouseX, self.mouseY)
            self.mouseX = None
            self.mouseY = None
            return Point(x, y)
        else:
            return None

    def getKey(self):
        """Дождитесь, пока пользователь нажмет клавишу, и верните ее в виде строки."""
        self.lastKey = ""
        while self.lastKey == "":
            self.update()
            if self.isClosed(): raise GraphicsError("getKey in closed window")
            time.sleep(.1)  # откажитесь от нити

        key = self.lastKey
        self.lastKey = ""
        return key

    def checkKey(self):
        """Возвращает последнее нажатие клавиши или нет, если с момента последнего вызова ни одна клавиша не нажималась"""
        if self.isClosed():
            raise GraphicsError("checkKey in closed window")
        self.update()
        key = self.lastKey
        self.lastKey = ""
        return key

    def getHeight(self):
        """Возвращает высоту окна"""
        return self.height

    def getWidth(self):
        """Возвращает ширину окна"""
        return self.width

    def toScreen(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.screen(x, y)
        else:
            return x, y

    def toWorld(self, x, y):
        trans = self.trans
        if trans:
            return self.trans.world(x, y)
        else:
            return x, y

    def setMouseHandler(self, func):
        self._mouseCallback = func

    def _onClick(self, e):
        self.mouseX = e.x
        self.mouseY = e.y
        if self._mouseCallback:
            self._mouseCallback(Point(e.x, e.y))

    def addItem(self, item):
        self.items.append(item)

    def delItem(self, item):
        self.items.remove(item)

    def redraw(self):
        for item in self.items[:]:
            item.undraw()
            item.draw(self)
        self.update()


class Transform:
    """Внутренний класс для двумерных преобразований координат"""

    def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
        # w, h - ширина и высота окна
        # (xlow,ylow) координаты нижнего левого [raw (0,h-1)]
        # (xhigh,yhigh) координаты верхнего правого  [raw (w-1,0)]
        xspan = (xhigh - xlow)
        yspan = (yhigh - ylow)
        self.xbase = xlow
        self.ybase = yhigh
        self.xscale = xspan / float(w - 1)
        self.yscale = yspan / float(h - 1)

    def screen(self, x, y):
        # Возвращает координаты x,y в экранных (фактически оконных) координатах
        xs = (x - self.xbase) / self.xscale
        ys = (self.ybase - y) / self.yscale
        return int(xs + 0.5), int(ys + 0.5)

    def world(self, xs, ys):
        # Возвращает xs,ys в мировых координатах
        x = xs * self.xscale + self.xbase
        y = self.ybase - ys * self.yscale
        return x, y


# Значения по умолчанию для различных параметров конфигурации элемента. Только подмножество
# ключи могут присутствовать в словаре конфигурации для данного элемента
DEFAULT_CONFIG = {"fill": "",
                  "outline": "black",
                  "width": "1",
                  "arrow": "none",
                  "text": "",
                  "justify": "center",
                  "font": ("helvetica", 12, "normal")}


class GraphicsObject:
    """Универсальный базовый класс для всех рисуемых объектов"""


    def __init__(self, options):
        # параметры - это список строк, указывающих, какие параметры являются

        # Когда объект нарисован, для canvas устанавливается значение GraphWin(холст)
        # объект, на котором он нарисован, и id - это идентификатор TK объекта
        # нарисованная фигура.
        self.canvas = None
        self.id = None

        # config - это словарь параметров конфигурации для виджета.
        config = {}
        for option in options:
            config[option] = DEFAULT_CONFIG[option]
        self.config = config

    def setFill(self, color):
        """Установите цвет интерьера на color"""
        self._reconfig("fill", color)

    def setOutline(self, color):
        """Установите цвет контура на color"""
        self._reconfig("outline", color)

    def setWidth(self, width):
        """Установите высоту линии в соответствие с шириной"""
        self._reconfig("width", width)

    def draw(self, graphwin):

        """Нарисуйте объект в graphwin, который должен быть GraphWin
        объект.  Графический объект может быть нарисован только в одном
    окне. Выдает ошибку при попытке нарисовать объект, который
    уже виден."""

        if self.canvas and not self.canvas.isClosed(): raise GraphicsError(OBJ_ALREADY_DRAWN)
        if graphwin.isClosed(): raise GraphicsError("Can't draw to closed window")
        self.canvas = graphwin
        self.id = self._draw(graphwin, self.config)
        graphwin.addItem(self)
        if graphwin.autoflush:
            _root.update()
        return self

    def undraw(self):

        """Разверните объект (т.е. спрячьте его). Возвращает автоматически, если
    объект в данный момент не нарисован."""

        if not self.canvas: return
        if not self.canvas.isClosed():
            self.canvas.delete(self.id)
            self.canvas.delItem(self)
            if self.canvas.autoflush:
                _root.update()
        self.canvas = None
        self.id = None

    def move(self, dx, dy):

        """переместите объект в единицах dx в направлении x и в единицах dy в вашем
        направление"""

        self._move(dx, dy)
        canvas = self.canvas
        if canvas and not canvas.isClosed():
            trans = canvas.trans
            if trans:
                x = dx / trans.xscale
                y = -dy / trans.yscale
            else:
                x = dx
                y = dy
            self.canvas.move(self.id, x, y)
            if canvas.autoflush:
                _root.update()

    def _reconfig(self, option, setting):

        if option not in self.config:
            raise GraphicsError(UNSUPPORTED_METHOD)
        options = self.config
        options[option] = setting
        if self.canvas and not self.canvas.isClosed():
            self.canvas.itemconfig(self.id, options)
            if self.canvas.autoflush:
                _root.update()

    def _draw(self, canvas, options):
        """рисует соответствующую фигуру на холсте с предоставленными опциями
        Возвращает идентификатор Tk нарисованного элемента"""
        pass

    def _move(self, dx, dy):
        """обновляет внутреннее состояние объекта для его перемещения в единицах dx,dy"""
        pass


class Point(GraphicsObject):
    def __init__(self, x, y):
        GraphicsObject.__init__(self, ["outline", "fill"])
        self.setFill = self.setOutline
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def _draw(self, canvas, options):
        x, y = canvas.toScreen(self.x, self.y)
        return canvas.create_rectangle(x, y, x + 1, y + 1, options)

    def _move(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy

    def clone(self):
        other = Point(self.x, self.y)
        other.config = self.config.copy()
        return other

    def getX(self): return self.x

    def getY(self): return self.y


class _BBox(GraphicsObject):


    def __init__(self, p1, p2, options=["outline", "width", "fill"]):
        GraphicsObject.__init__(self, options)
        self.p1 = p1.clone()
        self.p2 = p2.clone()

    def _move(self, dx, dy):
        self.p1.x = self.p1.x + dx
        self.p1.y = self.p1.y + dy
        self.p2.x = self.p2.x + dx
        self.p2.y = self.p2.y + dy

    def getP1(self): return self.p1.clone()

    def getP2(self): return self.p2.clone()

    def getCenter(self):
        p1 = self.p1
        p2 = self.p2
        return Point((p1.x + p2.x) / 2.0, (p1.y + p2.y) / 2.0)


class Rectangle(_BBox):

    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        return "Rectangle({}, {})".format(str(self.p1), str(self.p2))

    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1, y1 = canvas.toScreen(p1.x, p1.y)
        x2, y2 = canvas.toScreen(p2.x, p2.y)
        return canvas.create_rectangle(x1, y1, x2, y2, options)

    def clone(self):
        other = Rectangle(self.p1, self.p2)
        other.config = self.config.copy()
        return other


class Oval(_BBox):

    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2)

    def __repr__(self):
        return "Oval({}, {})".format(str(self.p1), str(self.p2))

    def clone(self):
        other = Oval(self.p1, self.p2)
        other.config = self.config.copy()
        return other

    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1, y1 = canvas.toScreen(p1.x, p1.y)
        x2, y2 = canvas.toScreen(p2.x, p2.y)
        return canvas.create_oval(x1, y1, x2, y2, options)


class Circle(Oval):

    def __init__(self, center, radius):
        p1 = Point(center.x - radius, center.y - radius)
        p2 = Point(center.x + radius, center.y + radius)
        Oval.__init__(self, p1, p2)
        self.radius = radius

    def __repr__(self):
        return "Circle({}, {})".format(str(self.getCenter()), str(self.radius))

    def clone(self):
        other = Circle(self.getCenter(), self.radius)
        other.config = self.config.copy()
        return other

    def getRadius(self):
        return self.radius


class Line(_BBox):

    def __init__(self, p1, p2):
        _BBox.__init__(self, p1, p2, ["arrow", "fill", "width"])
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        return "Line({}, {})".format(str(self.p1), str(self.p2))

    def clone(self):
        other = Line(self.p1, self.p2)
        other.config = self.config.copy()
        return other

    def _draw(self, canvas, options):
        p1 = self.p1
        p2 = self.p2
        x1, y1 = canvas.toScreen(p1.x, p1.y)
        x2, y2 = canvas.toScreen(p2.x, p2.y)
        return canvas.create_line(x1, y1, x2, y2, options)

    def setArrow(self, option):
        if not option in ["first", "last", "both", "none"]:
            raise GraphicsError(BAD_OPTION)
        self._reconfig("arrow", option)


class Polygon(GraphicsObject):

    def __init__(self, *points):
        # if points passed as a list, extract it
        if len(points) == 1 and type(points[0]) == type([]):
            points = points[0]
        self.points = list(map(Point.clone, points))
        GraphicsObject.__init__(self, ["outline", "width", "fill"])

    def __repr__(self):
        return "Polygon" + str(tuple(p for p in self.points))

    def clone(self):
        other = Polygon(*self.points)
        other.config = self.config.copy()
        return other

    def getPoints(self):
        return list(map(Point.clone, self.points))

    def _move(self, dx, dy):
        for p in self.points:
            p.move(dx, dy)

    def _draw(self, canvas, options):
        args = [canvas]
        for p in self.points:
            x, y = canvas.toScreen(p.x, p.y)
            args.append(x)
            args.append(y)
        args.append(options)
        return GraphWin.create_polygon(*args)


class Text(GraphicsObject):

    def __init__(self, p, text):
        GraphicsObject.__init__(self, ["justify", "fill", "text", "font"])
        self.setText(text)
        self.anchor = p.clone()
        self.setFill(DEFAULT_CONFIG['outline'])
        self.setOutline = self.setFill

    def __repr__(self):
        return "Text({}, '{}')".format(self.anchor, self.getText())

    def _draw(self, canvas, options):
        p = self.anchor
        x, y = canvas.toScreen(p.x, p.y)
        return canvas.create_text(x, y, options)

    def _move(self, dx, dy):
        self.anchor.move(dx, dy)

    def clone(self):
        other = Text(self.anchor, self.config['text'])
        other.config = self.config.copy()
        return other

    def setText(self, text):
        self._reconfig("text", text)

    def getText(self):
        return self.config["text"]

    def getAnchor(self):
        return self.anchor.clone()

    def setFace(self, face):
        if face in ['helvetica', 'arial', 'courier', 'times roman']:
            f, s, b = self.config['font']
            self._reconfig("font", (face, s, b))
        else:
            raise GraphicsError(BAD_OPTION)

    def setSize(self, size):
        if 5 <= size <= 36:
            f, s, b = self.config['font']
            self._reconfig("font", (f, size, b))
        else:
            raise GraphicsError(BAD_OPTION)

    def setStyle(self, style):
        if style in ['bold', 'normal', 'italic', 'bold italic']:
            f, s, b = self.config['font']
            self._reconfig("font", (f, s, style))
        else:
            raise GraphicsError(BAD_OPTION)

    def setTextColor(self, color):
        self.setFill(color)


class Entry(GraphicsObject):

    def __init__(self, p, width):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        # print self.anchor
        self.width = width
        self.text = tk.StringVar(_root)
        self.text.set("")
        self.fill = "gray"
        self.color = "black"
        self.font = DEFAULT_CONFIG['font']
        self.entry = None

    def __repr__(self):
        return "Entry({}, {})".format(self.anchor, self.width)

    def _draw(self, canvas, options):
        p = self.anchor
        x, y = canvas.toScreen(p.x, p.y)
        frm = tk.Frame(canvas.master)
        self.entry = tk.Entry(frm,
                              width=self.width,
                              textvariable=self.text,
                              bg=self.fill,
                              fg=self.color,
                              font=self.font)
        self.entry.pack()
        # self.setFill(self.fill)
        self.entry.focus_set()
        return canvas.create_window(x, y, window=frm)

    def getText(self):
        return self.text.get()

    def _move(self, dx, dy):
        self.anchor.move(dx, dy)

    def getAnchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Entry(self.anchor, self.width)
        other.config = self.config.copy()
        other.text = tk.StringVar()
        other.text.set(self.text.get())
        other.fill = self.fill
        return other

    def setText(self, t):
        self.text.set(t)

    def setFill(self, color):
        self.fill = color
        if self.entry:
            self.entry.config(bg=color)

    def _setFontComponent(self, which, value):
        font = list(self.font)
        font[which] = value
        self.font = tuple(font)
        if self.entry:
            self.entry.config(font=self.font)

    def setFace(self, face):
        if face in ['helvetica', 'arial', 'courier', 'times roman']:
            self._setFontComponent(0, face)
        else:
            raise GraphicsError(BAD_OPTION)

    def setSize(self, size):
        if 5 <= size <= 36:
            self._setFontComponent(1, size)
        else:
            raise GraphicsError(BAD_OPTION)

    def setStyle(self, style):
        if style in ['bold', 'normal', 'italic', 'bold italic']:
            self._setFontComponent(2, style)
        else:
            raise GraphicsError(BAD_OPTION)

    def setTextColor(self, color):
        self.color = color
        if self.entry:
            self.entry.config(fg=color)


class Image(GraphicsObject):
    idCount = 0
    imageCache = {}

    def __init__(self, p, *pixmap):
        GraphicsObject.__init__(self, [])
        self.anchor = p.clone()
        self.imageId = Image.idCount
        Image.idCount = Image.idCount + 1
        if len(pixmap) == 1:  # file name provided
            self.img = tk.PhotoImage(file=pixmap[0], master=_root)
        else:  # width and height provided
            width, height = pixmap
            self.img = tk.PhotoImage(master=_root, width=width, height=height)

    def __repr__(self):
        return "Image({}, {}, {})".format(self.anchor, self.getWidth(), self.getHeight())

    def _draw(self, canvas, options):
        p = self.anchor
        x, y = canvas.toScreen(p.x, p.y)
        self.imageCache[self.imageId] = self.img  # save a reference
        return canvas.create_image(x, y, image=self.img)

    def _move(self, dx, dy):
        self.anchor.move(dx, dy)

    def undraw(self):
        try:
            del self.imageCache[self.imageId]  # allow gc of tk photoimage
        except KeyError:
            pass
        GraphicsObject.undraw(self)

    def getAnchor(self):
        return self.anchor.clone()

    def clone(self):
        other = Image(Point(0, 0), 0, 0)
        other.img = self.img.copy()
        other.anchor = self.anchor.clone()
        other.config = self.config.copy()
        return other

    def getWidth(self):
        """Возвращает ширину изображения в пикселях"""
        return self.img.width()

    def getHeight(self):
        """Возвращает высоту изображения в пикселях"""
        return self.img.height()

    def getPixel(self, x, y):
        """Возвращает список [r,g,b] со значениями цвета RGB для пикселей (x,y)
        r,g,b находятся в диапазоне(256)"""

        value = self.img.get(x, y)
        if type(value) == type(0):
            return [value, value, value]
        elif type(value) == type((0, 0, 0)):
            return list(value)
        else:
            return list(map(int, value.split()))

    def setPixel(self, x, y, color):
        """Устанавливает пикселю (x,y) заданный цвет"""
        self.img.put("{" + color + "}", (x, y))

    def save(self, filename):
        """Сохраняет пиксельное изображение в формате filename.
Формат сохраняемого изображения определяется по расширению имени файла."""

        path, name = os.path.split(filename)
        ext = name.split(".")[-1]
        self.img.write(filename, format=ext)


def color_rgb(r, g, b):
    """r,g,b - интенсивности красного, зеленого и синего цветов в диапазоне(256)
Возвращает строку спецификатора цвета для результирующего цвета"""
    return "#%02x%02x%02x" % (r, g, b)



