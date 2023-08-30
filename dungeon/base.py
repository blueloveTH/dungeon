class Rect:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def width(self) -> int:
        return self.right - self.left
    
    def height(self) -> int:
        return self.bottom - self.top
    
    def area(self) -> int:
        return self.width() * self.height()
    
    def intersect(self, other: 'Rect') -> 'Rect':
        return Rect(
            max(self.left, other.left),
            max(self.top, other.top),
            min(self.right, other.right),
            min(self.bottom, other.bottom)
        )