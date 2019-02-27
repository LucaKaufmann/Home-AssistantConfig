"""
Camera that highlights the detected regions from the Tensorflow image processor
"""
import asyncio
import io
import logging
import os

import voluptuous as vol

from homeassistant.const import CONF_NAME
from homeassistant.components.camera import Camera, PLATFORM_SCHEMA
from homeassistant.helpers import config_validation as cv
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components.image_processing.tensorflow import ATTR_MATCHES
from homeassistant.loader import get_component
from PIL import Image, ImageDraw

_LOGGER = logging.getLogger(__name__)

ATTR_CAMERA = 'camera_entity'
ATTR_PROCESSOR = 'processor_entity'

CONF_CAMERA = 'camera'
CONF_COLOR = 'color'
CONF_PROCESSOR = 'processor'
CONF_CLASSIFIER = 'classifier'

DEFAULT_COLOR = (255, 255, 0)
DEFAULT_NAME = 'Tensorflow'
COLORS = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_CAMERA): cv.entity_id,
    vol.Required(CONF_PROCESSOR): cv.entity_id,
    vol.Optional(CONF_CLASSIFIER, default=None): cv.string,
    vol.Optional(CONF_COLOR, default=DEFAULT_COLOR): (int, int, int)
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Tensorflow camera platform."""
    add_devices([TensorflowCamera(hass, config.get(CONF_NAME, DEFAULT_NAME),
                             config[CONF_CAMERA], config[CONF_PROCESSOR],
                             config[CONF_CLASSIFIER], config[CONF_COLOR])])


class TensorflowCamera(Camera):
    """Visual representation of Tensorflow matched regions."""
    def __init__(self, hass, name, camera, processor, classifier, color):
        """Initialize the Tensorflow camera."""
        super().__init__()
        self._hass = hass
        self._camera = camera
        self._processor = processor
        self._color = color
        self._name = name
        self._classifier = classifier

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name

    @property
    def state_attributes(self):
        """Return the device state attributes."""
        return {
            ATTR_CAMERA: self._camera,
            ATTR_PROCESSOR: self._processor
        }

    async def async_camera_image(self):
        """Return the camera image still."""

        camera = self._hass.components.camera
        img = None
        processor = self._hass.states.get(self._processor)

        try:
            img = await camera.async_get_image(self._camera)
            

        except HomeAssistantError as err:
            _LOGGER.error("Error on receive image from entity: %s", err)
            return

        matches = processor.attributes.get(ATTR_MATCHES)
        regions = []
        i = 0
        for key, value in matches.items():
            color = COLORS[i]
            for match in value:
                region = match["box"]
                regions.append({"label": key, "region": region, "color": color})
            # for box in value:
            #     regions.append(region)
            i += 1

        stream = io.BytesIO(img.content)
        im = Image.open(stream)
        annotated_image = ImageDraw.Draw(im)
        width, height = im.size
        for region in regions:
            label = region["label"]
            box = region["region"]
            y0 = box[0]*height
            x0 = box[1]*width
            y1 = box[2]*height
            x1 = box[3]*width
            annotated_image.rectangle([x0, y0, x1, y1],
                                    outline=region["color"])
            annotated_image.text((x0+5,y0+5), label, region["color"])

        image_bytes = io.BytesIO()
        im.save(image_bytes, format='PNG')
        return image_bytes.getvalue()