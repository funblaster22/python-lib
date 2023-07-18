from typing import Tuple, Union


# TODO: make return types numpy immutable arrays? (.setflags(write=False))
class Box:
    _tk = None
    __tk_canvas = None
    
    def __init__(self, *, xywh: Tuple[int, int, int, int]=None, xyxy: Tuple[int, int, int, int]=None, ccwh: Tuple[int, int, int, int]=None, box: "Box"=None):
        self.__x1 = self.__x2 = self.__y1 = self.__y2 = self.__w = self.__h = self.__cx = self.__cy = 0
        self.set_pos(xywh=xywh, xyxy=xyxy, ccwh=ccwh, box=box)
        # This is the window for drawing 

    def set_pos(self, *, xywh: Tuple[int, int, int, int]=None, xyxy: Tuple[int, int, int, int]=None, ccwh: Tuple[int, int, int, int]=None, box: "Box"=None):
        if xywh is not None:
            self.x1, self.y1, self.w, self.h = xywh
        elif xyxy is not None:
            self.x1, self.y1, self.x2, self.y2 = xyxy
        elif ccwh is not None:
            cx, cy, w, h = ccwh
            self.x1 = cx - w / 2
            self.y1 = cy - h / 2
            self.w, self.h = (w, h)
        elif box is not None:
            self.x1, self.y1, self.x2, self.y2 = (box.x1, box.y1, box.x2, box.y2)
        self.__set_center()

    """ TODO: can this be written more efficiently w/o recursion? I think reverse should only be used internally, which isn't clear """
    def chk_collision(self, other: "Box", *, reverse=True) -> bool:
        if ((other.x1 < self.x1 < other.x2 or other.x1 < self.x2 < other.x2)
            and (other.y1 < self.y1 < other.y2 or other.y1 < self.y2 < other.y2))\
                or (reverse and other.chk_collision(self, reverse=False)):
            return True
        return False

    def moveBy(self, dx: int, dy: int):
        # __x1 and __y1 were set manually, but caused boxes to shrink in deal/no solver, so I changed it
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def show(self, module=None, frame=None, color=None, thickness=2):
        """ If module and frame is None, create a debugging tkinter window. The only backend that is currently implemented is openCV """
        if module is None:  # TODO: This method is untested because I forgot all Tkinter, I'm too tired, & I should be doing college apps
            from tkinter import Tk, Canvas
            if self._tk is None:
                type(self)._tk = Tk()
                type(self).__tk_canvas = Canvas(self._tk)
                self.__tk_canvas.pack(fill="both", expand=True)
            self.__tk_canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline="black" if color is None else color)
            width = max(self._tk.winfo_width(), self.x2) + 5
            height = max(self._tk.winfo_height(), self.y2) + 5
            self._tk.geometry(str(width) + "x" + str(height))
        elif module.__name__ == "cv2.cv2":
            module.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), (0,0,255) if color is None else color, thickness)

    def includes(self, x: int, y: int):
        """Checks if a coordinate is inside the Box"""
        return self.x1 < x < self.x2 and self.y1 < y < self.y2

    @staticmethod
    def intersection(one: "Box", two: "Box") -> "Box":
        """Note: even if the boxes don't intersect, this will return a Box with 0 area & all vertices are the rightmost corner of box two. Same if they share an edge. I chose this behavior over returning None because null checks are very inconvenient"""
        x1 = max(one.x1, two.x1)
        y1 = max(one.y1, two.y1)
        x2 = min(one.x2, two.x2)
        y2 = min(one.y2, two.y2)
        # This is important because otherwise, it will falsely recognise overlap if box 2 is less than box 1
        if x1 <= x2 and y1 <= y2:
            return Box(xyxy=(x1, y1, x2, y2))
        else:
            return Box(xyxy=(0, 0, 0, 0))

    def __set_center(self):
        self.__cx = self.x1 + self.w / 2
        self.__cy = self.y1 + self.h / 2

    def __str__(self):
        out = "Box("
        for key, val in self.__dict__.items():  # __dir__ was producing too much output
            unmangledKey = key.split("__")[-1]  # Remove private field prefix
            out += unmangledKey + "=" + str(val) + ", "
        out = out[0:len(out)-2]
        out += ")"
        return out

    def __repr__(self):
        return str(self)

    def __sub__(self, other: "Box") -> Tuple[int, int]:
        return int(self.cx - other.cx), int(self.cy - other.cy)

    def __bool__(self):
        return self.xyxy != (0, 0, 0, 0)

    def __eq__(self, other):
        """Note: will not try to approximate doubles"""
        return self.xyxy == other.xyxy

    def __mul__(self, other: Union[float, int]):
        box = Box(xyxy=(self.x1 * other, self.y1 * other, self.x2 * other, self.y2 * other))
        if isinstance(other, int):
            return box.int()
        return box

    def __truediv__(self, other: Union[float, int]):
        return self * (1 / other)

    def int(self):
        return Box(xyxy=(int(self.x1), int(self.y1), int(self.x2), int(self.y2)))

    @property
    def slicer(self):
        return slice(self.y1, self.y2, None), slice(self.x1, self.x2, None)  # Equivalent to np.s_[y1:y2, x1:x2]

    @property
    def xyxy(self):
        return self.x1, self.y1, self.x2, self.y2

    @property
    def xywh(self):
        return self.x1, self.y1, self.w, self.h

    @property
    def ccwh(self):
        return self.cx, self.cy, self.w, self.h

    @property
    def center(self):
        return self.cx, self.cy

    @center.setter
    def center(self, newCenter: tuple[int, int]):
        self.cx, self.cy = newCenter

    @property
    def size(self):
        return self.w, self.h

    @size.setter
    def size(self, newSize: tuple[int, int]):
        self.w, self.h = newSize

    @property
    def x1(self):
        return int(self.__x1)

    @x1.setter
    def x1(self, x1):
        self.__x1 = x1
        try:
            self.__w = self.__x2 - self.__x1
        finally:
            self.__set_center()

    @property
    def y1(self):
        return int(self.__y1)

    @y1.setter
    def y1(self, y1):
        self.__y1 = y1
        try:
            self.__h = self.__y2 - self.__y1
        finally:
            self.__set_center()

    @property
    def x2(self):
        return int(self.__x2)

    @x2.setter
    def x2(self, x2):
        self.__x2 = x2
        try:
            self.__w = self.__x2 - self.__x1
        finally:
            self.__set_center()

    @property
    def y2(self):
        return int(self.__y2)

    @y2.setter
    def y2(self, y2):
        self.__y2 = y2
        try:
            self.__h = self.__y2 - self.__y1
        finally:
            self.__set_center()

    @property
    def w(self):
        return int(self.__w)

    @w.setter
    def w(self, w):
        self.__w = w
        try:
            self.__x2 = self.__x1 + self.__w
        finally:
            self.__set_center()

    @property
    def h(self):
        return int(self.__h)

    @h.setter
    def h(self, h):
        self.__h = h
        try:
            self.__y2 = self.__y1 + self.__h
        finally:
            self.__set_center()

    @property
    def cx(self):
        return int(self.__cx)

    @cx.setter
    def cx(self, cx):
        self.moveBy(cx - self.cx, 0)

    @property
    def cy(self):
        return int(self.__cy)

    @cy.setter
    def cy(self, cy):
        self.moveBy(0, cy - self.cy)

    @property
    def area(self) -> float:
        return self.__w * self.__h

    @property
    def perimeter(self) -> float:
        return 2 * self.__w + 2 * self.__h


if __name__ == "__main__":
    box = Box(xywh=(0, 0, 30, 10))
    box2 = Box(xyxy=(2, 2, 50, 4))
    print("Collision:", box.chk_collision(box2), box2.chk_collision(box))
    box = Box(xywh=(0, 0, 10, 10))
    box2 = Box(xywh=(10, 10, 10, 10))
