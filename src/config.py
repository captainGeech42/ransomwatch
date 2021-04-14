import os
from typing import Dict
import yaml

with open(os.getenv("RW_CONFIG_PATH", "config.yaml"), "r") as f:
    Config: Dict = yaml.load(f, Loader=yaml.CLoader)