# HomeAssistant-Config
Example configuration for HomeAssistant. Using the following components:

- Philips Hue
- Xiaomi
- Darksky
- iOS component
- Google Cast
- Plex
- HAFloorplan

My setup is running on a Raspberry Pi along with Homebridge (for Homekit integration), Pihole ad blocker and OpenVPN. DuckDNS and Letsencrypt are set up as well to allow access from outside the network.

# Node Red flows
Node Red automations are backed up in the flows.json file.
Here's an overview:
![Node red flows](https://github.com/LucaKaufmann/Home-AssistantConfig/raw/master/light_automations.png)

Media lights automations:
![Node red flows](https://github.com/LucaKaufmann/Home-AssistantConfig/raw/master/media_lights_automations.png)

Vacuum automations:

![Node red flows](https://github.com/LucaKaufmann/Home-AssistantConfig/raw/master/vacuum_automations.png)

AC automations:

![Node red flows](https://github.com/LucaKaufmann/Home-AssistantConfig/raw/master/AC_automations.png)
