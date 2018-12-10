"""
Support for Netatmo Smart Thermostat.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/climate.netatmo/
"""
import logging
from datetime import timedelta
import voluptuous as vol

from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
import custom_components.netatmo2 as netatmo2
from homeassistant.components.climate import (
    STATE_HEAT, STATE_IDLE, ClimateDevice, PLATFORM_SCHEMA,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_OPERATION_MODE, SUPPORT_AWAY_MODE)
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv


# STATE_AUTO = 'Schedule'
# STATE_ECO = 'Away'
# STATE_MANUAL = 'manual'
# STATE_HIGH_DEMAND = 'max'
# STATE_OFF = 'off'

# DICT_NETATMO_TO_HA = {
#     'schedule': STATE_AUTO,
#     'away': STATE_ECO,
#     'manual': STATE_MANUAL,
#     'max': STATE_HIGH_DEMAND,
#     'off': STATE_OFF,
# }

# OPERATION_LIST = [STATE_AUTO, STATE_ECO,
#                   STATE_MANUAL, STATE_HIGH_DEMAND]

DEPENDENCIES = ['netatmo2']

_LOGGER = logging.getLogger(__name__)

CONF_HOMES = 'homes'
CONF_ROOMS = 'rooms'

# DEFAULT_AWAY_TEMPERATURE = 14
# # The default offset is 2 hours (when you use the thermostat itself)
# DEFAULT_TIME_OFFSET = 7200
# # Return cached results if last scan was less then this time ago
# # NetAtmo Data is uploaded to server every hour
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOMES): cv.string,
    vol.Optional(CONF_ROOMS, default=[]):
        vol.All(cv.ensure_list, [cv.string]),
})

SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE |
                 SUPPORT_AWAY_MODE)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the NetAtmo Thermostat."""
    netatmo = hass.components.netatmo2
    home = config.get(CONF_HOMES)

    import lnetatmo
    try:
        home_data = HomeData(netatmo.NETATMO_AUTH, home)
        for home in home_data.get_home_names():
            room_data = ThermostatData(netatmo.NETATMO_AUTH, home)
            for room_name in room_data.get_room_names():
                if CONF_ROOMS in config:
                    if config[CONF_ROOMS] != [] and \
                       room_name not in config[CONF_ROOMS]:
                        continue
                add_entities([NetatmoThermostat(room_data, room_name)], True)
    except lnetatmo.NoDevice:
        return None


class NetatmoThermostat(ClimateDevice):
    """Representation a Netatmo thermostat."""

    def __init__(self, data, room_name, away_temp=None):
        """Initialize the sensor."""
        self._data = data
        self._state = None
        self._name = 'test_' + room_name
        self._target_temperature = None
        self._away = None
        self._operation_list = ['Schedule', 'Manual', 'Max',
                                'Hg']
        self._operation_mode = None
        # self._boiler_status = None
        self.update_without_throttle = False

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._data.current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature

    @property
    def current_operation(self):
        """Return the current state of the thermostat."""
        state = self._data.boilerstatus
        if state is False:
            return STATE_IDLE
        elif state is True:
            return STATE_HEAT
        # if self._operation_mode == 'hg':
        #     return 'Hg'
        # elif self._operation_mode == 'manual':
        #     return STATE_MANUAL
        # elif self._operation_mode == 'max':
        #     return STATE_HIGH_DEMAND
        # elif self._operation_mode == 'off':
        #     return STATE_OFF
        # elif self._operation_mode == 'schedule':
        #     return STATE_AUTO
        # elif self._operation_mode == 'away':
        #     print('tis echt wel ze')
        #     return STATE_ECO

    # @property
    # def boiler_status(self):
    #     """Return the current state of the thermostat."""
    #     state = self._data.boilerstatus
    #     if state is False:
    #         self._boiler_status = STATE_IDLE
    #     elif state is True:
    #         self._boiler_status = STATE_HEAT
    #     return self._boiler_status

    @property
    def operation_list(self):
        """Return the operation modes list."""
        return self._operation_list

    @property
    def operation_mode(self):
        """Return current operation ie. heat, cool, idle."""
        # print('kust men gat')
        # print('self._operation_mode', self._data.setpoint_mode)
        if self._operation_mode == 'hg':
            return 'Hg'
        elif self._operation_mode == 'manual':
            return 'Manual'
        elif self._operation_mode == 'max':
            return 'Max'
        elif self._operation_mode == 'off':
            return 'Off'
        elif self._operation_mode == 'schedule':
            return 'Schedule'
        elif self._operation_mode == 'away':
            # print('tis echt wel ze')
            return 'Away'

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        if self._data.thermostat_type == 'NATherm1':
            return {
                "home_id": self._data.home_id,
                "room_id": self._data.room_id,
                "setpoint_default_duration": self._data.setpoint_duration,
                "away_temperature": self._data.away_temperature,
                "hg_temparature": self._data.hg_temparature,
                "operation_mode": self._operation_mode,
                "boiler_status": self.current_operation,
                "thermostat_type": self._data.thermostat_type,
                "module_id": self._data.module_id
                }
        elif self._data.thermostat_type != 'NATherm1':
            return {
                "home_id": self._data.home_id,
                "room_id": self._data.room_id,
                "setpoint_default_duration": self._data.setpoint_duration,
                "away_temperature": self._data.away_temperature,
                "hg_temparature": self._data.hg_temparature,
                "operation_mode": self._operation_mode,
                "thermostat_type": self._data.thermostat_type,
                "module_id": self._data.module_id
                }

    @property
    def is_away_mode_on(self):
        """Return true if away mode is on."""
        # print('kak away')
        return self._away

    def turn_away_mode_on(self):
        """Turn away on."""
        mode = "away"
        self._data.homestatus.setThermmode(home_id=self._data.home_id, mode=mode)
        self._data.homestatus.setroomThermpoint(home_id=self._data.home_id, room_id=self._data.room_id, mode=mode)
        self.update_without_throttle = True
        # self._away = True

    def turn_away_mode_off(self):
        """Turn away off."""
        mode = "schedule"
        self._data.homestatus.setThermmode(home_id=self._data.home_id, mode=mode)
        self.update_without_throttle = True
        # self._away = False

    def set_operation_mode(self, operation_mode):
        """Set HVAC mode (auto, auxHeatOnly, cool, heat, off)."""
        # print('operation_mode', operation_mode)
        if operation_mode == 'Off':
            self._data.homestatus.setroomThermpoint(home_id=self._data.home_id, room_id=self._data.room_id, mode='off')
        elif operation_mode == 'Max':
            self._data.homestatus.setroomThermpoint(home_id=self._data.home_id, room_id=self._data.room_id, mode='max')
        elif operation_mode == 'Hg':
            self._data.homestatus.setThermmode(home_id=self._data.home_id, mode='hg')
            # self._data.homestatus.setroomThermpoint(home_id=self._data.home_id, room_id=self._data.room_id, mode='hg')
        elif operation_mode == 'Schedule':
            self._data.homestatus.setThermmode(self._data.home_id, 'schedule')
            # self._data.homestatus.setroomThermpoint(self._data.home_id, self._data.room_id, 'schedule')
        self.update_without_throttle = True

    def set_temperature(self, **kwargs):
        """Set new target temperature for 2 hours."""
        temp = kwargs.get(ATTR_TEMPERATURE)
        if temp is None:
            return
        mode = "manual"
        self._data.homestatus.setroomThermpoint(home_id=self._data.home_id, room_id=self._data.room_id,
             mode=mode, temp=temp)
        self.update_without_throttle = True
        # self._target_temperature = temp
        # self._away = False

    # @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from NetAtmo API and updates the states."""
        if self.update_without_throttle:
            self._data.update(no_throttle=True)
            self.update_without_throttle = False
        else:
            self._data.update()
        # print('self._data.setpoint_mode', self._data.setpoint_mode)
        # self._target_temperature = self._data.homestatus.setPoint()
        self._target_temperature = self._data.target_temperature
        self._away = self._data.setpoint_mode == 'away'
        # print('self._away', self._away)
        self._operation_mode = self._data.setpoint_mode
        self.operation_mode


class HomeData(object):
    """        """
    def __init__(self, auth, home=None):
        self.auth = auth
        self.homedata = None
        self.home_names = []
        self.room_names = []
        self.schedules = []
        self.home = home
        self.home_id = None

    def get_home_names(self):
        self.setup()
        for home in self.homedata.homes:
            if 'modules' in self.homedata.homes[home]:
                self.home_names.append(self.homedata.homes[home]['name'])
        return self.home_names

    def setup(self):
        import lnetatmo
        self.homedata = lnetatmo.HomeData(self.auth)
        self.home_id = self.homedata.gethomeId(home=self.home)


class ThermostatData(object):
    """Get the latest data from Netatmo."""

    def __init__(self, auth, home=None):
        """Initialize the data object."""
        self.auth = auth
        self.homedata = None
        self.homestatus = None
        self.home_names = []
        self.room_names = []
        self.schedules = []
        self.home = home
        self.current_temperature = None
        self.away_temperature = None
        self.hg_temparature = None
        self.target_temperature = None
        self.setpoint_mode = None
        self.boilerstatus = None
        self.setpoint_duration = None

    def get_room_names(self):
        """Return all module available on the API as a list."""
        # self.update()
        self.setup()
        for room in self.homestatus.rooms:
            self.room_id = self.homestatus.rooms[room]['id']
            if self.home in self.homedata.rooms:
                roomName = self.homedata.rooms[self.home][self.room_id]['name']
                self.room_names.append(roomName)

        return self.room_names

    # def get_schedules_names(self):
    #     self.update()

    def setup(self):
        import lnetatmo
        self.homedata = lnetatmo.HomeData(self.auth)
        self.homestatus = lnetatmo.HomeStatus(self.auth, home=self.home)
        self.home_id = self.homedata.gethomeId(home=self.home)

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Call the NetAtmo API to update the data."""
        import lnetatmo
        self.homestatus = lnetatmo.HomeStatus(self.auth, home=self.home)
        self.target_temperature = self.homestatus.setPoint(rid=self.room_id)
        self.setpoint_mode = self.homestatus.setPointmode(rid=self.room_id)
        self.current_temperature = self.homestatus.measuredTemperature(rid=self.room_id)
        self.away_temperature = self.homestatus.getAwaytemp(home=self.home)
        self.hg_temparature = self.homestatus.getHgtemp(home=self.home)
        # self.boilerstatus = self.homestatus.boilerStatus()
        self.thermostat_type = self.homestatus.thermostatType(home=self.home, rid=self.room_id)
        self.module_id = self.homestatus.module_id
        self.setpoint_duration = self.homedata.setpoint_duration[self.home]
        if self.thermostat_type == 'NATherm1':
            self.boilerstatus = self.homestatus.boilerStatus(rid=self.module_id)
        # print('self.target_temperature', self.target_temperature)
        # print('self.setpoint_mode', self.setpoint_mode)
        # print('self.current_temperature', self.current_temperature)
        # print('self.away_temperature', self.away_temperature)
        # print('self.hg_temparature', self.hg_temparature)
        # print('self.boilerstatus', self.boilerstatus)
        # print('self.setpoint_duration', self.setpoint_duration)
