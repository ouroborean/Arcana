import typing

if typing.TYPE_CHECKING:
    from arcana.game_event import GameEvent

class Dialogue():
    
    def __init__(self, text: str, speaker = None, choices: list[str] = list(), events: list["GameEvent"] = list()):
        self.text = text
        self.events = events
        self.choices = choices
        self.speaker = speaker
    
    @property
    def longest_choice(self) -> str:
        longest_choice = ""
        for choice in self.choices:
            if len(choice) > len(longest_choice):
                longest_choice = choice
        return longest_choice

class Conversation():
    
    dialogue: list[Dialogue]
    active_panel: int
    choices_made: list[str]
    
    def __init__(self, dialogue: list[Dialogue]):
        self.dialogue = dialogue
        self.active_panel = 0
        self.choices_made = list()
    
    @property
    def active(self):
        return self.dialogue[self.active_panel]
        
    def confirm(self, choice):
        if self.active.choices:
            self.choices_made.append(self.active.choices[choice])
        self.progress_conversation()
            
    
    def progress_conversation(self):
        self.active_panel += 1
        print(self.active_panel)
        if self.active_panel == len(self.dialogue):
            print("Conversation over")
            return False
        else:
            return True
