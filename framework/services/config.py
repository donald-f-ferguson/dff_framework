# Copyright 2024 -- Donald F. Ferguson
#
import os
from typing import Any


class Config:
    """
    A very simple class for implementing the 12 Factor App guideline III. Config -- Store config in the environment.

    The current implementation simply wraps os.environ for getting most config properties. There is support to
    add an entry. A service factory my add entries.

    In the future, we will add other options, for example calling a secrets manager.
    """

    def __init__(self):
        self.config = dict()

    def get_config(self, config_name:str) -> Any:
        """
        Get a configuration value. First check if a value was explicitly set. Otherwise,
        get the value from an environment variable.

        :param config_name: The name of the configuration value/property.
        :return: The value.
        """
        result = self.config.get(config_name, None)
        if result is None:
            result = os.environ.get(config_name, None)
        return result

    def set_config(self, config_name: str, config_value: Any) -> None:
        """
        Set a configuration value.

        :param config_name: The variables name.
        :param config_value: The value.
        :return: None
        """
        self.config[config_name] = config_value

