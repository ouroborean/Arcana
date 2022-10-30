from arcana.area import *

def test_area_one():
    area = area_db["test"]
    tilemap = area.gen_tilemap()
    assert len(tilemap.portals) == 1
    assert tilemap.portals[0].loc == (12, 7)

def test_area_two():
    area = area_db["test2"]
    tilemap = area.gen_tilemap()
    assert len(tilemap.portals) == 1
    assert  2 <= tilemap.portals[0].x <= 5
    assert 2 <= tilemap.portals[0].y <= 8
    
