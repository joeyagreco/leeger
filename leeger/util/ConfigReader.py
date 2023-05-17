import configparser
import os
from typing import Optional

from leeger.util.CustomLogger import CustomLogger


class ConfigReader:
    """
    Used to read from .properties files
    """

    @staticmethod
    def get(
        section: str, name: str, *, asType: type = str, propFile: str = "app.properties"
    ) -> Optional[str | int | float | bool]:
        LOGGER = CustomLogger().getLogger()
        configParser = configparser.ConfigParser()
        propertiesDirectory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "../properties")
        )
        configParser.read(os.path.join(propertiesDirectory, propFile))
        value = None
        try:
            value = configParser[section][name]
            value = asType(value)
        except Exception as e:
            LOGGER.error(e)
        return value
