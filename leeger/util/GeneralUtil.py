from typing import Any, Optional

from leeger.util.ConfigReader import ConfigReader
from leeger.util.CustomLogger import CustomLogger
from leeger.util.Deci import Deci


class GeneralUtil:
    @staticmethod
    def filter(*, value: Any, list_: list) -> list:
        """
        Filters out the given value from the given list.
        """
        return [v for v in list_ if v is not value]

    @staticmethod
    def warnForUnusedKwargs(
        kwargs: dict[str, Any], *, excludeKeys: Optional[list[str]] = None
    ) -> None:
        """
        Logs a warning for each present kwarg in the given dict.
        Will ignore kwargs with a key in excludeKeys.
        """
        LOGGER = CustomLogger.getLogger()

        excludeKeys = excludeKeys if excludeKeys is not None else list()
        # get the list of common kwargs that sometimes linger in kwargs to be passed down and used later.
        defaultExcludeKeys = ConfigReader.get("KWARGS", "WARNING_EXCLUDE_KEYS", asType=list)
        excludeKeys += defaultExcludeKeys

        unused_kwargs = [kwarg for kwarg in kwargs.keys() if kwarg not in excludeKeys]
        for kwarg in unused_kwargs:
            LOGGER.warning(f"Keyword argument '{kwarg}' unused.")

    @staticmethod
    def safeSum(*numbers) -> Optional[Deci | int | float]:
        """
        Safely adds numbers where None is ignored.
        Examples:
            * 1 + None = 1
            * None + 1 = 1
            * None + None = None
            * 1 + 1 = 2
        """
        safeSum = None
        for number in numbers:
            if None in (safeSum, number):
                safeSum = number if safeSum is None else safeSum
            else:
                safeSum += number

        return safeSum

    def findDifferentFields(
        dict1: dict,
        dict2: dict,
        *,
        parentKey: str = "",
        ignoreKeyNames: Optional[list[str]] = None,
        isRootDict: bool = True,
    ) -> list[str]:
        """
        Finds the differences in the dicts and returns them.
        Uses dot notation, i.e. 'foo.baz.bar'
        """
        differentFields = []

        if ignoreKeyNames is None:
            ignoreKeyNames = []

        for key in dict1:
            fullKey = f"{parentKey}.{key}" if parentKey else key

            value1 = dict1[key]
            value2 = dict2[key]

            if isinstance(value1, dict) and isinstance(value2, dict):
                isRootDict = False
                differentFields.extend(
                    GeneralUtil.findDifferentFields(
                        value1,
                        value2,
                        parentKey=fullKey,
                        ignoreKeyNames=ignoreKeyNames,
                        isRootDict=isRootDict,
                    )
                )
            elif isinstance(value1, (list, tuple)) and isinstance(value2, (list, tuple)):
                if len(value1) != len(value2):
                    differentFields.append((fullKey, (value1, value2)))
                else:
                    list_differences = []
                    for i in range(len(value1)):
                        if isinstance(value1[i], dict) and isinstance(value2[i], dict):
                            nested_diff = GeneralUtil.findDifferentFields(
                                value1[i],
                                value2[i],
                                parentKey=f"{fullKey}[{i}]",
                                ignoreKeyNames=ignoreKeyNames,
                                isRootDict=False,
                            )
                            differentFields.extend(nested_diff)
                        elif value1[i] != value2[i]:
                            list_differences.append(i)
                    if len(list_differences) == len(value1):
                        differentFields.append((fullKey, (value1, value2)))
                    elif list_differences:
                        for index in list_differences:
                            differentFields.append(
                                (f"{fullKey}[{index}]", (value1[index], value2[index]))
                            )
            elif value1 != value2 and key not in ignoreKeyNames:
                differentFields.append((fullKey, (value1, value2)))

        return differentFields
