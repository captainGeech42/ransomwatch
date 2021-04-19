import logging
import socket
import time
from typing import Union

import requests
from stem import Signal
from stem.control import Controller
from stem.util.log import get_logger

from config import Config

class Proxy:
    controller: Union[Controller, None]
    ip: str
    hostname: str
    socks_port: int
    ctrl_port: int
    password: str

    session: requests.Session

    def __init__(self):
        self.hostname = Config["proxy"]["hostname"]
        self.socks_port = Config["proxy"]["socks_port"]
        self.ctrl_port = Config["proxy"]["control_port"]
        self.password = Config["proxy"]["password"]

        self.controller = None
        self.ip = ""

        logger = get_logger()
        logger.level = logging.WARNING
    
    def __enter__(self):
        self.connect()

        return self

    def __exit__(self, *args):
        self.close()

    def connect(self) -> None:
        # get the IP of the proxy container
        # stem doesn't support connecting using the hostname for some reason
        self.ip = socket.gethostbyname(self.hostname)

        # connect to tor control port
        self.controller = Controller.from_port(address = self.ip, port = self.ctrl_port)

        # auth to control
        self.controller.authenticate(password = self.password)

        # initialize requests session
        self.new_session()

    def close(self) -> None:
        assert(self.controller is not None)

        self.controller.close()

    def reconnect(self) -> None:
        assert(self.controller is not None)

        self.controller.close()

        # connect to tor control port
        self.controller = Controller.from_port(address = self.ip, port = self.ctrl_port)

        # auth to control
        self.controller.authenticate(password = self.password)

        # initialize requests session
        self.new_session()

    def new_identity(self) -> None:
        assert(self.controller is not None)

        # request new identity
        self.controller.signal(Signal.NEWNYM)

        # wait for circuit to be established
        time.sleep(self.controller.get_newnym_wait())

        # need to reset session after establishing a new circuit
        self.new_session()

    def new_session(self) -> None:
        assert(self.controller is not None)

        self.session = requests.Session()

        # socks5h forces requests to do DNS over the proxy
        # https://gist.github.com/jefftriplett/9748036#gistcomment-2291558
        self.session.proxies.update({
            "http": f"socks5h://{self.hostname}:{self.socks_port}",
            "https": f"socks5h://{self.hostname}:{self.socks_port}"
        })

    def get(self, *args, **kwargs) -> requests.Response:
        return self.session.get(*args, **kwargs)

    def post(self, *args, **kwargs) -> requests.Response:
        return self.session.post(*args, **kwargs)

    def put(self, *args, **kwargs) -> requests.Response:
        return self.session.put(*args, **kwargs)

    def patch(self, *args, **kwargs) -> requests.Response:
        return self.session.patch(*args, **kwargs)

    def delete(self, *args, **kwargs) -> requests.Response:
        return self.session.delete(*args, **kwargs)

    def head(self, *args, **kwargs) -> requests.Response:
        return self.session.head(*args, **kwargs)
