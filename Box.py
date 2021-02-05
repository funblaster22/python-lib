from typing import Tuple


class Box:
    def __init__(self, *, xywh: Tuple[int, int, int, int]=None, xyxy: Tuple[int, int, int, int]=None, ccwh: Tuple[int, int, int, int]=None, box: "Box"=None):
        self.__x1 = self.__x2 = self.__y1 = self.__y2 = self.__w = self.__h = self.__cx = self.__cy = 0
        self.set_pos(xywh=xywh, xyxy=xyxy, ccwh=ccwh, box=box)

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

    def chk_collision(self, other: "Box", *, reverse=True) -> bool:
        if ((other.x1 < self.x1 < other.x2 or other.x1 < self.x2 < other.x2)
            and (other.y1 < self.y1 < other.y2 or other.y1 < self.y2 < other.y2))\
                or (reverse and other.chk_collision(self, reverse=False)):
            return True
        return False

    def moveBy(self, dx: int, dy: int):
        self.__x1 += dx
        self.__y1 += dy
        self.x2 += dx
        self.y2 += dy

    def moveTo(self, *, x1y1: Tuple[int, int]=None, cxcy: Tuple[int, int]=None):
        if x1y1 is not None:
            transform = (x1y1[0] - self.x1, x1y1[1] - self.y1)
        elif cxcy is not None:
            transform = (cxcy[0] - self.cx, cxcy[1] - self.cy)
        else:
            transform = (0, 0)
        self.moveBy(*transform)

    def show(self, module, frame, color=(0,0,255)):
        if module.__name__ == "cv2.cv2":
            module.rectangle(frame, (self.x1, self.y1), (self.x2, self.y2), color, 2)

    def __set_center(self):
        self.__cx = self.x1 + self.w / 2
        self.__cy = self.y1 + self.h / 2

    def __str__(self):
        out = "Box("
        for key, val in self.__dict__.items():  # __dir__ was producing too much output
            out += key[6:] + "=" + str(val) + ", "
        out = out[0:len(out)-2]
        out += ")"
        return out

    def __repr__(self):
        return str(self)

    def __sub__(self, other: "Box") -> Tuple[int, int]:
        return int(self.cx - other.cx), int(self.cy - other.cy)

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
