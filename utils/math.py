from pygame.math import Vector2
import numpy as np

class Rect2():
    """
    Spans a rectangle from 4 points.
         ul *----------------* ur
           /                  \
          /                    \
         /                      \
        /                        \
    ll *--------------------------* lr
    """
    def __init__(self, ul: Vector2, ur: Vector2, ll: Vector2, lr: Vector2):
        self.ul = ul # Upper left
        self.ur = ur # Upper right
        self.ll = ll # Lower left
        self.lr = lr # Lower right

    def __init__(self):
        self.ul = Vector2(0, 0)
        self.ur = Vector2(1, 0)
        self.ll = Vector2(0, 1)
        self.lr = Vector2(1, 1)

    def __str__(self):
        return f"Rect2(ul={self.ul}, ur={self.ur}, ll={self.ll}, lr={self.lr})"

    def __iter__(self):
        return [self.ul, self.ur, self.ll, self.lr].__iter__()
    
    def set(self, data):
        self.ul.x = data.get("upper_left", {}).get("x", 0)
        self.ul.y = data.get("upper_left", {}).get("y", 0)

        self.ur.x = data.get("upper_right", {}).get("x", 1)
        self.ur.y = data.get("upper_right", {}).get("y", 0)

        self.ll.x = data.get("lower_left", {}).get("x", 0)
        self.ll.y = data.get("lower_left", {}).get("y", 1)

        self.lr.x = data.get("lower_right", {}).get("x", 1)
        self.lr.y = data.get("lower_right", {}).get("y", 1)

    def to_numpy_array(self):
        return np.array([[self.ul.x, self.ul.y], # Upper left
                         [self.ur.x, self.ur.y],
                         [self.ll.x, self.ll.y],
                         [self.lr.x, self.lr.y]], dtype=np.float32)

