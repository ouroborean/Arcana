from arcana.tile import Tile, TileStatus
from arcana.direction import Direction, offset_to_direction, direction_to_offset
from arcana.scenery import Scenery, Portal

import random
from typing import Tuple

class TileMap():
    
    tile: list[Tile]
    width: int
    height: int
    portals: list
    prefabs: set
    
    def __init__(self, dimensions: Tuple[int, int]):
        self.width, self.height = dimensions
        self.tiles = [None] * (self.width * self.height)
        self.portals = list()
        self.enemies = list()
        self.prefabs = set()
        
    def is_border_tile(self, i) -> bool:
        return i % self.width == 0 or i % self.width == self.width - 1 or i // self.width == 0 or i // self.width == self.height - 1
    
    def valid_coord(self, coord) -> bool:
        return (coord[0] + (coord[1] * self.width)) >= 0 and (coord[0] + (coord[1] * self.width)) < (self.width*self.height) and coord[0] < self.width and coord[1] < self.height and coord[0] >= 0 and coord[1] >= 0
    
    def add_tile(self, tile:Tile, location:Tuple):
        """Adds a tile to the tilemap at a specific location, and populates its neighbor dictionary based on all tiles currently existing around it"""
        
        #If input value is a coordinate pair, set it as the true location and get the index location from the coordinate
        #If input value is an index, set it as the index location and get the true location from the index value
        if isinstance(location, Tuple):
            true_loc = location
            num_loc = self.coord_to_num(location)
        elif isinstance(location, int):
            true_loc = self.num_to_coord(location)
            num_loc = location
        
        #set the tile's location
        tile.set_loc(true_loc)
        
        #initialize a few cute little tuples to loop through all the possible border offsets
        x = (-1, 0, 1)
        y = (-1, 0, 1)
        
        #Loop through the offsets to assign neighbor tiles to the tile we're currently adding
        for offset1 in x:
            offset_x = true_loc[0] + offset1
            for offset2 in y:
                offset_y = true_loc[1] + offset2
                if not (offset1, offset2) == (0, 0) and self.get_tile((offset_x, offset_y)):
                    tile.set_neighbor(offset_to_direction((offset1, offset2)), self.get_tile((offset_x, offset_y)))

        self.tiles[num_loc] = tile
        
    def add_scenery(self, scenery, tile):
        if tile.scenery:
            tile.remove_scenery()
        tile.apply_scenery(scenery)
        
    def add_scenery_to_adjacent_tile(self, current_tile, scenery, direction):
        location = current_tile + direction_to_offset(direction)
        if self.valid_coord(location):
            self.add_scenery(scenery, self.get_tile(location))
            
    def add_scenery_in_line(self, scenery_components, origin, direction, length):
        source_tile = self.get_tile(origin)
        source_tile.apply_scenery(Scenery(*scenery_components))
        for _ in range(length - 1):
            new_coord = source_tile + direction_to_offset(direction)
            if not self.valid_coord(new_coord):
                break
            self.add_scenery_to_adjacent_tile(source_tile, Scenery(*scenery_components), direction)
            source_tile = self.get_tile(new_coord)
    
    def add_adjacent_tile(self, current_tile, new_tile, direction):
        location = current_tile + direction_to_offset(direction)
        if self.valid_coord(location):
            self.add_tile(new_tile, location)
    
    def add_tiles_in_line(self, new_tile_components, origin, direction, length):
        source_tile = Tile(*new_tile_components)
        self.add_tile(source_tile, origin)
        for _ in range(length - 1):
            if not self.valid_coord(source_tile + direction_to_offset(direction)):
                break
            new_tile = Tile(*new_tile_components)
            self.add_adjacent_tile(source_tile, new_tile, direction)
            source_tile = new_tile
    
    def add_tiles_by_prefab(self, prefab, origin):
        for tile in prefab.tiles:
            if tile:
                tile.mark_as_prefab()
                coord = tile + origin
                self.add_tile(tile, coord)
                
    
    def get_tile(self, coord: Tuple[int, int]) -> Tile:
        if self.valid_coord(coord):
            return self.tiles[coord[0] + (coord[1] * self.width)]
        
    def get_shortest_path(self, start, end) -> list[Tile]:
        """A* pathing algorithm. Returns the shortest list of tiles (counting the start and end point) between the two given Tiles."""
        
        open_nodes = list()
        closed_nodes = set()
        
        #add the start point to the list of open nodes to check
        open_nodes.append(start)  
        
        ROOK_TILES = (Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST)
        BISHOP_TILES = (Direction.NORTHEAST, Direction.NORTHWEST, Direction.SOUTHEAST, Direction.SOUTHWEST)
        while True:
            #Sort open nodes so that the Tile with the lowest F-Cost (total of H and G costs) is at the front. If there's a tie,
            #sort by the lowest H-cost (crow-fly distance to goal)
            open_nodes.sort(key= lambda x: (x.f_cost, x.h_cost))
            
            #if we've run out of open, valid nodes to check, there is no valid path. Return an empty list.
            if not open_nodes:
                return []
            
            #Get the front node with the aforementioned appropriate values
            current = open_nodes.pop(0)
            #add this node to the closed node list, so we won't check it again.
            closed_nodes.add(current)
            #if this node is the targeted end node, we're done.
            if current == end:
                break
            
            #check each neighbor tile for the current tile. If that node does not currently have a g-cost, or if the g-cost of our
            #current node + the amount it would increase by traveling to that tile would be less than its current g-cost, give it
            #new G and H-costs, set its parent to the current node to be traversed when we have the completed path, and add it to
            #the list of open nodes.
            for direction, node in current.neighbor.items():
                if node and node.walkable:
                    if node in closed_nodes:
                        continue
                    if direction in ROOK_TILES:
                        path_length = 10
                    elif direction in BISHOP_TILES:
                        path_length = 14
                    if current.g_cost + path_length < node.g_cost or not node in open_nodes:
                        node.set_g_cost(current.g_cost + path_length)
                        node.set_h_cost(end)
                        node.parent = current
                        if not node in open_nodes:
                            open_nodes.append(node)
        
        #we'll build the list backwards, traversing from the end to the start by checking each node's assigned parent.
        #Then, we reverse the list and return it
        output = [end]
        while not start in output:
            output.append(output[-1].parent)
        output.reverse()
        return output
    
    def carpet_tile_map(self, tiles, prefab_count):
        """Cover the tilemap in tiles, randomly chosen from the provided constructors and random weights."""
        odds = (self.width * self.height) // prefab_count
        for i in range(self.width * self.height):
            roll = random.randint(1, 100)
            for weight, details in tiles.items():
                if roll <= weight:
                    tile = Tile(*details)
                    roll = random.randint(1, odds)
                    if roll == 1:
                        tile.marked_for_prefab = True
                    self.add_tile(tile, self.num_to_coord(i))
                    break
                else:
                    roll -= weight
    
    def border_tile_map(self, args):
        for i in range(self.width * self.height):
            if i % self.width == 0 or i % self.width == self.width - 1 or i // self.width == 0 or i // self.width == self.height - 1:
                self.get_tile(self.num_to_coord(i)).apply_scenery(Scenery(*args))
    
    
    def add_prefab(self, prefabs):
        prefab_markers = [tile for tile in self.tiles if tile.marked_for_prefab]
        for tile in prefab_markers:
            for odds, prefab in prefabs.items():
                roll = random.randint(1, 100)
                newfab = prefab()
                if roll <= odds and not newfab.name in self.prefabs:
                    origin = (tile.loc[0] - newfab.entrance_loc[0], tile.loc[1] - newfab.entrance_loc[1])
                    if self.space_for_prefab(newfab, origin):
                        self.add_tiles_by_prefab(newfab, origin)
                        self.prefabs.add(newfab.name)
                else:
                    roll -= odds
                    
    def space_for_prefab(self, prefab, origin):
        for tile in prefab.tiles:
            if tile:
                if not self.valid_coord(tile + origin) or self.get_tile(tile + origin).prefab:
                    return False
        for portal in self.portals:
            if not self.get_shortest_path(self.get_tile(portal.loc), self.get_tile((prefab.entrance_loc[0] + origin[0], prefab.entrance_loc[1] + origin[1]))):
                return False
        return True
    
    def add_random_scenery(self, scenery, clutter_seed):
        for i in range(self.width * self.height):
            if not self.is_border_tile(i):
                roll = random.randint(1, 100)
                if roll <= clutter_seed:
                    roll = random.randint(1, 100)
                    for weight, details in scenery.items():
                        if roll <= weight:
                            self.get_tile(self.num_to_coord(i)).apply_scenery(Scenery(*details))
                            break
                        else:
                            roll -= weight
                            
    def add_portals(self, portal_package):
        for package in portal_package:
            # if there's only one tuple in the first part of the package,
            # it's a guaranteed coordinate for the portal
            if len(package[0]) == 1:
                portal = Portal(*package[1])
                self.get_tile(*package[0]).remove_scenery()
                self.get_tile(*package[0]).apply_scenery(portal)
                portal.lock_location(*package[0])
                self.portals.append(portal)
            elif len(package[0]) > 1:
                #if there's more than one tuple in the first part of the package,
                #the tuples are a rectangular bounding box for a random placement of
                #the portal
                
                first_corner = package[0][0]
                width = package[0][1][0]
                height = package[0][1][1]
                portal = Portal(*package[1])
                tiles_in_rect = list()
                for x in range(width):
                    for y in range(height):
                        tiles_in_rect.append(self.get_tile((first_corner[0] + x, first_corner[1] + y)))
                dest = random.choice(tiles_in_rect)
                dest.remove_scenery()
                dest.apply_scenery(portal)
                portal.lock_location(dest.loc)
                self.portals.append(portal)
    
    def num_to_coord(self, num: int) -> Tuple[int, int]:
        return (num % self.width, num // self.width)
    
    def coord_to_num(self, coord: Tuple[int, int]) -> int:
        return coord[0] + (coord[1] * self.width)
    