

class Actor():
    
    def __init__(self):
        self.loc = (0, 0)
        self.current_health = 0
        self.is_new = True
        self.sight_range = 0
    
    def in_sight_range(self, tile, pathing_func):
        eyes = self.sight_range
        x_diff = abs(self.x - tile.x)
        eyes -= x_diff
        y_diff = abs(self.y - tile.y)
        eyes -= y_diff
        if eyes < 0:
            return False
        else:
            path = pathing_func(tile, self.loc, crow=True)[1:]
            for tile in path:
                if tile.scenery and 1 in tile.scenery.status:
                    return False
        return True    

    @property
    def dead(self) -> bool:
        return self.current_health <= 0