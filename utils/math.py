class Vector2():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2({self.x:.2f}, {self.y:.2f})"

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

    def __str__(self):
        return f"Rect2(ul={self.ul}, ur={self.ur}, ll={self.ll}, lr={self.lr})"

