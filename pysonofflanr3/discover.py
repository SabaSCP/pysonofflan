import ipaddress
import time
from typing import Dict
from datetime import datetime
from zeroconf import ServiceBrowser, Zeroconf


class Discover:

    @staticmethod
    async def discover(logger, seconds_to_wait=5) -> Dict[str, str]:
        """
        :rtype: dict
        :return: Array of devices {"device_id", "ip:port"}
        """
        logger.debug("Looking for all eWeLink devices on local network.")

        zeroconf = Zeroconf()
        listener = MyListener(logger)
        ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener)

        time.sleep(seconds_to_wait)

        zeroconf.close()

        return listener.devices


class MyListener:

    def __init__(self, logger):
        self._logger = logger
        self.devices = {}

    def add_service(self, zeroconf, service_type, name):
        self._logger.debug("%s - Service %s added" % (datetime.now(), name))
        info = zeroconf.get_service_info(service_type, name)
        self._logger.debug(info)
        device = info.properties[b"id"].decode("ascii")
        ip = f'{ipaddress.ip_address(info.addresses[0])}:{info.port}'

        self._logger.info(
            "Found Sonoff LAN Mode device %s at socket %s" % (device, ip)
        )

        self.devices[device] = ip

    def update_service(self, zeroconf, service_type, name):
        pass

    def remove_service(self, zeroconf, service_type, name):
        pass
