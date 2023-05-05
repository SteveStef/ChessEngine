

class Tile:
    def __init__(self, value, isHidden):
        self.value = value
        self.hidden = isHidden
    
    def isBomb(self):
        return self.value == "X"

    def __str__(self):
        return f"{self.value}"

