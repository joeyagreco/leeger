import configparser
import os
from typing import Optional


class ConfigReader:
    """
    Used to read from .properties files
    """

    @staticmethod
    def get(
        section: str, name: str, *, asType: str | list = str, propFile: str = "app.properties"
    ) -> Optional[str | int | float | bool]:
        configParser = configparser.ConfigParser(
            converters={"list": lambda x: [i.strip() for i in x.split(",")]}
        )
        propertiesDirectory = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "../properties")
        )
        configParser.read(os.path.join(propertiesDirectory, propFile))
        value = None
        # cast as type
        if asType == list:
            value = configParser.getlist(section, name)
        elif asType == str:
            value = configParser[section][name]
        else:
            raise ValueError(f"Type '{asType}' not supported for conversion.")
        return value
