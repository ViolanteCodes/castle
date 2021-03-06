"""This file contains the base design of most of the models used in the
game."""

# the get_line_number function is used to assist with error tracking.
from inspect import currentframe
def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

class Player():
    """A simple representation of the protagonist."""
    def __init__(self, name='', inventory=[], entered =[]):
        self.name = name
        self.inventory = inventory
        self.entered = entered

    def enter_room(self, room):
        self.current_room = room
        if room not in self.entered:
            print(f"\n\t{room.entry_text}")
            self.entered.append(room)
        else:
            print(f"\n\tYou are back in the {self.current_room}.")
    
    def get_name(self):
        if self.name == '':
            self.name = input('Hello, player. What is your name?')
        else:
            print(self.name)
    
    def look_room(self):
        print(f"\n\t{self.current_room.description}")
        for item in self.current_room.room_inventory:
            if item.hidden != True:
                print(f"\n\t{item.text_in_room}")    

    def __str__(self):
        return 'player'

class Object():
    """A simple representation of an in-game object."""
    def __init__(
        self,
        slug='',
        # An abbreviated name for the object.
        description='',
        # Description given during 'look' method.
        text_in_room = '',
        # Text added to room description
        can_pickup=False,
        # Specifies whether the object can be picked up.
        can_use = False,
        # Specifies whether an object can be used at all.
        use_with='',
        # Specifies what other objects with object can be used with.
        use_alone=False,
        # Specifies if the object can be used alone.
        only_in_room = [],
        # Specifies if there is a specific room that the item has to 
        # be used in and what the updated text would be.
        use_text='',
        # Specifies what text is displayed with this object is used via
        # the use_object method.
        used=False,
        # Flag updated after object is used.
        updated_description = '',
        # Updated description, needed if object changes after use.
        cant_pickup_text = "You can't pick that up.",
        # Set to a default, can be customized for specific instances.
        use_once = False,
        # Destroys the object after use if True.
        hidden = False,
        # Sets the item as hidden.
        ):
        self.slug = slug
        self.description = description
        self.text_in_room = text_in_room
        self.can_pickup = can_pickup
        self.can_use = can_use
        self.use_with = use_with
        self.use_alone = use_alone
        self.only_in_room = only_in_room
        self.use_text = use_text
        self.used = used
        self.updated_description = updated_description
        self.cant_pickup_text = cant_pickup_text
        self.text_in_room = text_in_room
        self.use_once = use_once
        self.hidden = hidden
    
    def __str__(self):
        return self.slug
        
    def look_object(self):
        print(f"\n\t{self.description}")
    
    def pickup_object(self, player):
        """Checks if object is available to be picked up; if so, adds to
        player_inventory and removed from room_inventory."""
        if self.can_pickup == False:
            print(f"\n\t{self.cant_pickup_text}")
        elif self in player.inventory:
            print(f"\n\tThe {self.slug} is already in your bag.")
        else:
            print(f"\n\tYou put the {self.slug} into your bag.")
            player.inventory.append(self)
            player.current_room.room_inventory.remove(self)
    
    def drop_object(self, player):
        """Checks if the object is in player_inventory, drops the 
        object into room inventory, and changes text_in_room."""
        if self in player.inventory:
            print(f"\n\tYou drop the {self.slug} on the ground.")
            player.current_room.room_inventory.append(self)
            player.inventory.remove(self)
            self.text_in_room = f" There is a {self.slug} on the ground."
    
    def use_it_alone(self, player):
        """Tries to use the object by itself."""
        if self.used == True:
            print(f"\n\tYou already used this.")
        elif self.can_use == False:
            print(f"\n\tYou're not sure how to use a {self.slug} right now.")
        elif self.use_alone == False:
            print(f"\n\tYou're not sure what to do with a {self.slug} right now. Maybe "
            "this object has to be used with something else.")
        elif self.only_in_room:
            if player.current_room.slug != self.only_in_room[0]:
                print(f"\n\t{self.use_text}")
            else:
                print(f"\n\t{self.only_in_room[1]}")
                self.used = True
                if self.updated_description:
                    self.description = self.updated_description
                if self.use_once == True:
                    player.inventory.remove(self)
        else: print(f"Uh oh, something went wrong: {get_linenumber()}.")
    
    def use_together(self, paired, player):
        """Try to use the object with another object."""
        if self.can_use == False:
            print(f"\n\tYou're not sure how to use a {self.slug} right now.")
        elif paired.can_use == False:
            print(f"\n\tYou're not sure how to use a {paired.slug} right now.")
        elif self.used == True:
            print(f"\n\tThe {self.slug} is already all used up.")
        elif paired.used == True:
            print(f"\n\tThe {paired.slug} is already all used up.")
        elif self.use_with != paired:
            print(f"\n\tYou're not sure how these go together.")
        elif self.use_with == paired:
            if self.use_text:
                print(f"\n\t{self.use_text}")
            if paired.use_text:
                print(f"\n\t{paired.use_text}")
            self.used = True
            paired.used = True
            if self.updated_description:
                self.description = self.updated_description
            if paired.updated_description:
                paired.description = paired.updated_description
            if self.use_once == True:
                if self in player.inventory:
                    player.inventory.remove(self)
                elif self in player.current_room.room_inventory:
                    player.current_room.room_inventory.remove(self)
            if paired.use_once == True:
                if paired in player.inventory:
                    player.inventory.remove(paired)
                elif paired in player.current_room.room_inventory:
                    player.current_room.room_inventory.remove(paired)

        else: print(f"Uh oh, something went wrong: {get_linenumber()}.")

class Door(Object):
    """Represents a door or exit to a room."""
    def __init__(self, slug, description, text_in_room, can_pickup, can_use,
    use_with, use_alone, only_in_room, use_text, used, updated_description, cant_pickup_text, use_once, hidden):
        """initalize attributes of the parent class"""
        super().__init__(self, slug, description, text_in_room, can_pickup, can_use,
        use_with, use_alone, only_in_room, use_text, used, updated_description, cant_pickup_text, use_once, hidden, paired_room)
        self.locked=True
        self.visible=False
        self.can_use=True
        self.use_alone=True
        self.paired_room = ''

    def use_it_alone(self, player):
        """Tries to use the door."""
        if self.locked == True:
            print(f"\n\tIt seems like this {self.slug} is locked.")
        elif self.use_alone == False:
            print(f"\n\tIt feels like you're missing something here.")
        else: 
            player.enter_room(player, self.paired_room)

    def use_together(self, paired, player):
        """Try to use the door with another object."""
        if self.can_use == False:
            print(f"\n\tYou're not sure how to use these right now.")
        elif self.use_with != paired.slug:
            print(f"\n\tThis combination doesn't seem to work.")
        elif self.use_with != paired.slug:
            return False
        elif self.use_with == paired.slug:
            print(f"\n\t{self.use_text}")
            self.used = True
            if self.updated_description:
                self.description = self.updated_description
            return True
        else: print(f"Uh oh, something went wrong: {get_linenumber()}.")

    def use_paired(self):
        """Alter the paired object if the main object is used."""
        self.used = True
        if self.updated_description:
            self.description = self.updated_description
        if self.use_once:
            player.inventory.remove(self)
    
class Room():
    """Model for a room or area tile in-game"""
    def __init__(self, slug, description='', entry_text='',  
    room_inventory=[], entered=False,):
        self.slug = slug
        self.description = description
        self.entry_text = entry_text
        self.room_inventory = room_inventory
        self.entered = entered

    def stage_items(self, staged=[]):
        for stage in staged:
            self.room_inventory.append(stage)
    
    def __str__(self):
        return self.slug