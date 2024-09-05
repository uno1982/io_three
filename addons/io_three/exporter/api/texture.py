from bpy import data, types
from .. import constants, logger
from .constants import IMAGE, MAG_FILTER, MIN_FILTER, MAPPING
from . import image

def _texture(func):
    """
    :param func:
    """
    def inner(name, *args, **kwargs):
        """
        :param name:
        :param *args:
        :param **kwargs:
        """
        if isinstance(name, types.Texture):
            texture = name
        else:
            texture = data.textures.get(name)
            if texture is None:
                logger.error(f"Texture {name} not found.")
                return None
        return func(texture, *args, **kwargs)
    return inner

@_texture
def anisotropy(texture):
    """
    :param texture:
    :return: filter_size value
    """
    logger.debug("texture.file_path(%s)", texture)
    return texture.filter_size

@_texture
def file_name(texture):
    """
    :param texture:
    :return: file name
    """
    logger.debug("texture.file_name(%s)", texture)
    if texture and texture.image:
        return image.file_name(texture.image)
    else:
        logger.error(f"Texture {texture.name if texture else 'unknown'} does not have an image.")
        return None

@_texture
def file_path(texture):
    """
    :param texture:
    :return: file path
    """
    logger.debug("texture.file_path(%s)", texture)
    if texture and texture.image:
        return image.file_path(texture.image)

@_texture
def image_node(texture):
    """
    :param texture:
    :return: texture's image node
    """
    logger.debug("texture.image_node(%s)", texture)
    return texture.image

@_texture
def mag_filter(texture):
    """
    :param texture:
    :return: THREE_mag_filter value
    """
    logger.debug("texture.mag_filter(%s)", texture)
    try:
        val = texture.THREE_mag_filter
    except AttributeError:
        logger.debug("No THREE_mag_filter attribute found")
        val = MAG_FILTER
    return val

@_texture
def mapping(texture):
    """
    :param texture:
    :return: THREE_mapping value
    """
    logger.debug("texture.mapping(%s)", texture)
    try:
        val = texture.THREE_mapping
    except AttributeError:
        logger.debug("No THREE_mapping attribute found")
        val = MAPPING
    return val

@_texture
def min_filter(texture):
    """
    :param texture:
    :return: THREE_min_filter value
    """
    logger.debug("texture.min_filter(%s)", texture)
    try:
        val = texture.THREE_min_filter
    except AttributeError:
        logger.debug("No THREE_min_filter attribute found")
        val = MIN_FILTER
    return val

@_texture
def repeat(texture):
    """The repeat parameters of the texture node
    :param texture:
    :returns: repeat_x, and repeat_y values
    """
    logger.debug("texture.repeat(%s)", texture)
    return (texture.repeat_x, texture.repeat_y)

@_texture
def wrap(texture):
    """The wrapping parameters of the texture node
    :param texture:
    :returns: tuple of THREE compatible wrapping values
    """
    logger.debug("texture.wrap(%s)", texture)
    wrapping = {
        True: constants.WRAPPING.MIRROR,
        False: constants.WRAPPING.REPEAT
    }
    return (wrapping[texture.use_mirror_x],
            wrapping[texture.use_mirror_y])

def textures():
    """
    :return: list of texture node names that are IMAGE
    """
    logger.debug("texture.textures()")
    for mat in data.materials:
        if mat.users == 0:
            continue
        if mat.use_nodes:
            for node in mat.node_tree.nodes:
                if node.type == 'TEX_IMAGE' and node.image:
                    yield node.image.name

class Texture:
    def __init__(self, name, scene):
        self.name = name
        self.scene = scene
        self.node = None
        self.image = None

        # Find the texture node
        for mat in bpy.data.materials:
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image and node.image.name == name:
                        self.node = node
                        self.image = node.image
                        break

        if self.node is None:
            logger.error(f"Texture {name} not found in any material nodes.")
            raise KeyError(f"Texture {name} not found")

        img_inst = self.scene.image(api.texture.file_name(self.node))
