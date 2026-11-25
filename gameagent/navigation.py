"""Navigation on synthetic maps using the upstream python-pathfinding API."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Map:
    cells: tuple
    start: tuple
    goal: tuple

MAPS = {
    "genshin_impact": Map(((1,1,0,1,1),(0,1,0,1,0),(1,1,1,1,1)),(0,0),(4,2)),
    "wuthering_waves": Map(((1,1,1,0),(0,0,1,1),(1,1,1,1)),(0,0),(3,2)),
    "neverness_to_everness": Map(((1,1,1,1,1),(1,0,0,0,1),(1,1,1,1,1)),(0,0),(4,2)),
}

def route(world):
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
    from pathfinding.core.diagonal_movement import DiagonalMovement
    if not world.cells or not world.cells[0] or any(len(row)!=len(world.cells[0]) for row in world.cells):
        raise ValueError("Invalid map")
    for x,y in (world.start,world.goal):
        if not (0<=y<len(world.cells) and 0<=x<len(world.cells[0]) and world.cells[y][x]>0):
            raise ValueError("Invalid endpoint")
    grid=Grid(matrix=[list(row) for row in world.cells])
    path,runs=AStarFinder(diagonal_movement=DiagonalMovement.never).find_path(grid.node(*world.start),grid.node(*world.goal),grid)
    return {"path":[[n.x,n.y] for n in path],"expanded":runs,"reachable":bool(path)}
