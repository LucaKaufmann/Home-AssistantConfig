"""
Component that performs TensorFlow classification on images.

For a quick start, pick a pre-trained COCO model from:
https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/image_processing.tensorflow/
"""
import logging
import sys
import os

import voluptuous as vol

from homeassistant.components.image_processing import (
    CONF_CONFIDENCE, CONF_ENTITY_ID, CONF_NAME, CONF_SOURCE, PLATFORM_SCHEMA,
    ImageProcessingEntity)
from homeassistant.core import split_entity_id
from homeassistant.helpers import template
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['numpy==1.15.3', 'pillow==5.2.0', 'protobuf==3.6.1']

_LOGGER = logging.getLogger(__name__)

ATTR_PEOPLE = 'people'
ATTR_NO_PEOPLE = 'no_people'
ATTR_STATE = 'state'

CONF_FILE_OUT = 'file_out'
CONF_MODEL = 'model'
CONF_GRAPH = 'graph'
CONF_LABELS = 'labels'
CONF_MODEL_DIR = 'model_dir'
CONF_CATEGORIES = 'categories'
CONF_CATEGORY = 'category'
CONF_AREA = 'area'
CONF_TOP = 'top'
CONF_LEFT = 'left'
CONF_BOTTOM = 'bottom'
CONF_RIGHT = 'right'

AREA_SCHEMA = vol.Schema({
    vol.Optional(CONF_TOP, default=0): cv.small_float,
    vol.Optional(CONF_LEFT, default=0): cv.small_float,
    vol.Optional(CONF_BOTTOM, default=1): cv.small_float,
    vol.Optional(CONF_RIGHT, default=1): cv.small_float
})

CATEGORY_SCHEMA = vol.Schema({
    vol.Required(CONF_CATEGORY): cv.string,
    vol.Optional(CONF_AREA): AREA_SCHEMA
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_FILE_OUT, default=[]):
        vol.All(cv.ensure_list, [cv.template]),
    vol.Required(CONF_MODEL): vol.Schema({
        vol.Required(CONF_GRAPH): cv.isfile,
        vol.Optional(CONF_LABELS): cv.isfile,
        vol.Optional(CONF_MODEL_DIR): cv.isdir,
        vol.Optional(CONF_AREA): AREA_SCHEMA,
        vol.Optional(CONF_CATEGORIES, default=[]):
            vol.All(cv.ensure_list, [vol.Any(
                cv.string,
                CATEGORY_SCHEMA
            )])
    })
})


def draw_box(draw, box, img_width,
             img_height, text='', color=(255, 255, 0)):
    """Draw bounding box on image."""
    ymin, xmin, ymax, xmax = box
    (left, right, top, bottom) = (xmin * img_width, xmax * img_width,
                                  ymin * img_height, ymax * img_height)
    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=5, fill=color)
    if text:
        draw.text((left, abs(top-15)), text, fill=color)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the TensorFlow image processing platform."""
    model_config = config.get(CONF_MODEL)
    model_dir = model_config.get(CONF_MODEL_DIR) \
        or hass.config.path('tensorflow')
    labels = model_config.get(CONF_LABELS) \
        or hass.config.path('tensorflow', 'object_detection',
                            'data', 'mscoco_label_map.pbtxt')

    # Make sure locations exist
    if not os.path.isdir(model_dir) or not os.path.exists(labels):
        _LOGGER.error("Unable to locate tensorflow models or label map.")
        return

    # append custom model path to sys.path
    sys.path.append(model_dir)

    try:
        # Verify that the TensorFlow Object Detection API is pre-installed
        # pylint: disable=unused-import,unused-variable
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        import tensorflow as tf # noqa
        from object_detection.utils import label_map_util # noqa
    except ImportError:
        # pylint: disable=line-too-long
        _LOGGER.error(
            "No TensorFlow Object Detection library found! Install or compile "
            "for your system following instructions here: "
            "https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md") # noqa
        return

    try:
        # Display warning that PIL will be used if no OpenCV is found.
        # pylint: disable=unused-import,unused-variable
        import cv2 # noqa
    except ImportError:
        _LOGGER.warning("No OpenCV library found. "
                        "TensorFlow will process image with "
                        "PIL at reduced resolution.")

    # setup tensorflow graph, session, and label map to pass to processor
    # pylint: disable=no-member
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(model_config.get(CONF_GRAPH), 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    session = tf.Session(graph=detection_graph)
    label_map = label_map_util.load_labelmap(labels)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=90, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    entities = []

    for camera in config[CONF_SOURCE]:
        entities.append(TensorFlowImageProcessor(
            hass, camera[CONF_ENTITY_ID], camera.get(CONF_NAME),
            session, detection_graph, category_index, config))

    add_entities(entities)


class TensorFlowImageProcessor(ImageProcessingEntity):
    """Representation of an TensorFlow image processor."""

    def __init__(self, hass, camera_entity, name, session, detection_graph,
                 category_index, config):
        """Initialize the TensorFlow entity."""
        model_config = config.get(CONF_MODEL)
        self.hass = hass
        self._camera_entity = camera_entity
        if name:
            self._name = name
        else:
            self._name = "TensorFlow {0}".format(
                split_entity_id(camera_entity)[1])
        self._session = session
        self._graph = detection_graph
        self._category_index = category_index
        self._min_confidence = config.get(CONF_CONFIDENCE)
        self._file_out = config.get(CONF_FILE_OUT)

        template.attach(hass, self._file_out)

        self._people = 0
        self._no_people = 0
        self._state = "Unknown"

    @property
    def camera_entity(self):
        """Return camera entity id from process pictures."""
        return self._camera_entity

    @property
    def name(self):
        """Return the name of the image processor."""
        return self._name

    @property
    def state(self):
        """Return the state of the entity."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return {
            ATTR_PEOPLE: self._people,
            ATTR_NO_PEOPLE: self._no_people,
            ATTR_STATE: self._state
        }

    def _save_image(self, image, matches, paths):
        from PIL import Image, ImageDraw
        import io
        img = Image.open(io.BytesIO(bytearray(image))).convert('RGB')
        img_width, img_height = img.size
        draw = ImageDraw.Draw(img)

        # Draw custom global region/area
        if self._area != [0, 0, 1, 1]:
            draw_box(draw, self._area,
                     img_width, img_height,
                     "Detection Area", (0, 255, 255))

        for category, values in matches.items():
            # Draw custom category regions/areas
            if (category in self._category_areas
                    and self._category_areas[category] != [0, 0, 1, 1]):
                label = "{} Detection Area".format(category.capitalize())
                draw_box(draw, self._category_areas[category], img_width,
                         img_height, label, (0, 255, 0))

            # Draw detected objects
            for instance in values:
                label = "{0} {1:.1f}%".format(category, instance['score'])
                draw_box(draw, instance['box'],
                         img_width, img_height,
                         label, (255, 255, 0))

        for path in paths:
            _LOGGER.info("Saving results image to %s", path)
            img.save(path)

    def read_tensor_from_image_file(self,
                                file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
        import tensorflow as tf

        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)
        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(
                file_reader, channels=3, name="png_reader")
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(
                tf.image.decode_gif(file_reader, name="gif_reader"))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
        else:
            image_reader = tf.image.decode_jpeg(
                file_reader, channels=3, name="jpeg_reader")
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result

    def process_image(self, image):
        """Process the image."""
        import numpy as np

        # try:
        #     import cv2  # pylint: disable=import-error
        #     img = cv2.imdecode(
        #         np.asarray(bytearray(image)), cv2.IMREAD_UNCHANGED)
        #     inp = img[:, :, [2, 1, 0]]  # BGR->RGB
        #     inp_expanded = inp.reshape(1, inp.shape[0], inp.shape[1], 3)
        # except ImportError:
        #     from PIL import Image
        #     import io
        #     img = Image.open(io.BytesIO(bytearray(image))).convert('RGB')
        #     img.thumbnail((460, 460), Image.ANTIALIAS)
        #     img_width, img_height = img.size
        #     inp = np.array(img.getdata()).reshape(
        #         (img_height, img_width, 3)).astype(np.uint8)
        #     inp_expanded = np.expand_dims(inp, axis=0)
#         for op in self._graph.get_operations():
#         	print(op.name)
#         	_LOGGER.info("Operation: %s", op.name)
        image_tensor = self.read_tensor_from_image_file('/images/xiaofang2/latest.jpg')
        input_operation = self._graph.get_operation_by_name('Placeholder')
        output_operation = self._graph.get_operation_by_name('final_result')

        results = self._session.run(output_operation.outputs[0], {
                input_operation.outputs[0]: image_tensor
            })
        results = np.squeeze(results)
        # results = self._session.run({image_tensor: inp_expanded})
        # results = np.squeeze(results)

        # matches = {}
        # total_matches = 0
        top_k = results.argsort()[-5:][::-1]
        for node_id in top_k:   
            score = results[node_id]
            score = score * 100
            if score > 100:
                score = 100
            if score < 1:
                score = 0
                
            if node_id == 1:
                self._people = score
                if score > 50:
                    self._state = "people"
                else:
                    self._state = "no_people"
            else:
                self._no_people = score
            _LOGGER.info('Label: %s Score: %s', node_id, score)
        # for result in results:
        #     score = score * 100
        #     boxes = box.tolist()

        #     # Exclude matches below min confidence value
        #     if score < self._min_confidence:
        #         continue

        #     # Exclude matches outside global area definition
        #     if (boxes[0] < self._area[0] or boxes[1] < self._area[1]
        #             or boxes[2] > self._area[2] or boxes[3] > self._area[3]):
        #         continue

        #     category = self._category_index[obj_class]['name']

        #     # Exclude unlisted categories
        #     if (self._include_categories
        #             and category not in self._include_categories):
        #         continue

        #     # Exclude matches outside category specific area definition
        #     if (self._category_areas
        #             and (boxes[0] < self._category_areas[category][0]
        #                  or boxes[1] < self._category_areas[category][1]
        #                  or boxes[2] > self._category_areas[category][2]
        #                  or boxes[3] > self._category_areas[category][3])):
        #         continue

        #     # If we got here, we should include it
        #     if category not in matches.keys():
        #         matches[category] = []
        #     matches[category].append({
        #         'score': float(score),
        #         'box': boxes
        #     })
        #     total_matches += 1

        # Save Images
#         if total_matches and self._file_out:
#             paths = []
#             for path_template in self._file_out:
#                 if isinstance(path_template, template.Template):
#                     paths.append(path_template.render(
#                         camera_entity=self._camera_entity))
#                 else:
#                     paths.append(path_template)
#             self._save_image(image, matches, paths)
# 
#         self._matches = matches
#         self._total_matches = total_matches
