
#Events

class GameEvent():
    def __init__(self):
        pass

class DialogueEvent():
    def __init__(self):
        pass
    
class SpawnEvent():
    def __init__(self):
        pass


#Triggers

class GameTrigger():
    def __init__(self):
        pass
    
class TileTrigger(GameTrigger):
    def __init__(self):
        pass
    
class InteractTrigger(GameTrigger):
    def __init__(self):
        pass
    
class CarryTrigger(GameTrigger):
    def __init__(self):
        pass
    
class DeathTrigger(GameTrigger):
    def __init__(self):
        pass
    
class TalkTrigger(GameTrigger):
    def __init__(self):
        pass
    
class TimerTrigger(GameTrigger):
    def __init__(self):
        pass

class FamilyTrigger(GameTrigger):
    def __init__(self):
        pass

class LinkTrigger(GameTrigger):
    def __init__(self):
        pass

    #types of triggers:
        #trigger on tile (trigger when a specified entity steps on a specified tile)
        #trigger on interact (trigger when a specified entity actions a specified bit of scenery)
        #trigger on carry (trigger when a specified item is held by a specified entity)
        #trigger on death (trigger when a specified entity is killed)