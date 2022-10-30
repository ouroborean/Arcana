

class Actor():
    
    def __init__(self):
        self.loc = (0, 0)
        self.current_health = 0
        self.is_new = True
        

    @property
    def dead(self) -> bool:
        return self.current_health <= 0