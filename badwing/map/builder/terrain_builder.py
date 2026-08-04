from crunge.engine.loader.tiled.builder.tile_layer_builder.polygon_terrain_builder import (
    PolygonTerrainBuilder,
)

#from ...tile import Tile, GhostTile, TerrainChunk
from crunge.engine.d2.entity.tile import Tile, GhostTile
from crunge.engine.d2.entity.terrain import TerrainChunk

class TerrainBuilder(PolygonTerrainBuilder):
    TERRAIN_TILE_TYPES = {
        "dirtCenter",
        "dirtHill_left",
        "dirtHill_right",
        "dirtCorner_left",
        "dirtCorner_right",
        "dirtHalf_mid",
    }

    def __init__(self):
        def create_node_cb(position, sprite, properties: dict):
            if properties.get("type") in self.TERRAIN_TILE_TYPES:
                return GhostTile(position, sprite)
            return Tile(position, sprite)

        def create_chunk_cb(points: list[tuple[float, float]]):
            return TerrainChunk(points)
        
        super().__init__(terrain_tile_types=self.TERRAIN_TILE_TYPES, create_node_cb=create_node_cb, create_chunk_cb=create_chunk_cb)
