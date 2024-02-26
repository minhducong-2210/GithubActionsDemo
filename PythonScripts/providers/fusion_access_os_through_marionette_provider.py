from PythonScripts.interfaces.iprovide_access_os import IProvideAccessOS
from ppv_pal.adapters.fusion_adapter import FusionAdapter
from time import sleep
import re


class FusionAccessOSThroughMarionetteProvider(IProvideAccessOS):
    def __init__(self, fusion_api, comm_type="SERIAL", port_number=10):
        # type: (FusionAdapter, str, int) -> None
        self._port_number = port_number
        self._fusion_api = fusion_api
        self._comm_type = comm_type
        self._delay = 2

    def execute_command(self, command, timeout, redirection, retries=1):
        response = None
        if redirection:
            for i in range(0, retries):
                try:
                    self._fusion_api.marionette.set_serial(self._port_number)
                    response = self._fusion_api.marionette.execute_command(command, timeout)
                    error_string = re.search(r'<error>(.*)</error>', response, re.DOTALL)
                    if re.match(r'^\s+$', error_string.group(1)):
                        break
                    sleep(self._delay)
                except Exception:
                    pass
        else:
            self._fusion_api.marionette.set_serial(self._port_number)
            self._fusion_api.marionette.execute_command_no_redirect(command)
        return response

    def current_os(self, retries):
        os = None
        for i in range(0, retries):
            try:
                self._fusion_api.marionette.set_serial(self._port_number)
                os = self._fusion_api.marionette.get_connected_os()
                if os != 'DISCONNECTED':
                    break
                sleep(self._delay)
            except Exception:
                pass
        return os

    def marionette_version(self, retries):
        version = None
        for i in range(0, retries):
            try:
                self._fusion_api.marionette.set_serial(self._port_number)
                version = self._fusion_api.marionette.get_agent_version()
                if version is not None:
                    break
                sleep(self._delay)
            except Exception:
                pass
        return version

    def port_config(self):
        if self._comm_type.upper() == "ETHERNET":
            self._fusion_api.marionette.set_ethernet_rcf()
        if self._comm_type.upper() == "SERIAL":
            self._fusion_api.marionette.set_serial(self._port_number)
        return True
