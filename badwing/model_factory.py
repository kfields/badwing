from loguru import logger
import glm
from pytmx import TiledMap, TiledTileLayer, TiledObjectGroup

from crunge.engine.math import Rect2i
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.resource.texture import Texture
from crunge.engine.loader.texture.image_texture_loader import ImageTextureLoader

from .scene_layer import SceneLayer

class ModelFactory:
    def __init__(self, layer: SceneLayer):
        self.layer = layer
        level = self.layer.level
        #self.map = level.map
        #self.map_layer = self.map.get_layer_by_name(self.layer.name)
        #logger.debug(f"map_layer: {self.map_layer}")

    def produce(self):
        #self.process_layer()
        pass

    def process_layer(self):
        map = self.map
        layer = self.map_layer
        name = map.filename
        tw = map.tilewidth
        th = map.tileheight
        mw = map.width
        mh = map.height - 1
        pixel_height = mh * th

        logger.debug(f"process_layer: {layer}")

        if isinstance(layer, TiledTileLayer):
            for x, y, gid in layer:
                y = mh - y
                x = x * tw
                y = y * th

                if gid:  # Ensure there's a tile at this location
                    # Retrieve the tile image
                    image = map.get_tile_image_by_gid(gid)
                    
                    # Retrieve custom properties for the tile
                    properties = map.get_tile_properties_by_gid(gid)
                    self.process_tile(glm.vec2(x, y), image, properties)
        elif isinstance(layer, TiledObjectGroup):
            for obj in layer:
                logger.debug(obj)
                # Retrieve the object image
                image = obj.image
                # Retrieve custom properties for the object
                properties = obj.properties
                self.process_object(glm.vec2(obj.x, pixel_height - obj.y), image, properties)

    def process_tile(self, position: glm.vec2, image, properties):
        #pass
        logger.debug(f"process_tile: {position}, {image}, {properties}")

    def process_object(self, position: glm.vec2, image, properties):
        #pass
        logger.debug(f"process_object: {position}, {image}, {properties}")