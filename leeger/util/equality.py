from typing import Any, Optional

from leeger.util.CustomLogger import CustomLogger
from leeger.util.GeneralUtil import GeneralUtil


def equals(
    *,
    objA: Any,
    objB: Any,
    baseFields: set[str],
    idFields: Optional[set[str]] = None,
    parentKey: str = "",
    ignoreIdFields: bool = False,
    logDifferences: bool = False,
    ignoreKeyNames: Optional[list[str]] = None,
    toJsonMethodName: str = "toJson",
) -> bool:
    """
    Checks if objA is the same as objB.

    objA: instance to compare
    objB: instance to compare
    baseFields: fields that must always match
    idFields: id fields that must sometimes match
    parentKey: name of the parent key to display in the differences log
    ignoreIds: whether to compare id fields or not
    logDifferences: whether to log differences in the case of inequality or not
    ignoreKeyNames: list of key names to ignore when logging differences
    toJsonMethodName: the name of the method to call on these objects that will return the JSON representation of it
    """
    LOGGER = CustomLogger.getLogger()

    equal = True
    for field in baseFields:
        equal = equal and getattr(objA, field) == getattr(objB, field)

    if not ignoreIdFields and idFields:
        for field in idFields:
            equal = equal and getattr(objA, field) == getattr(objB, field)

    if not equal and logDifferences:
        ignoreKeyNames = list() if ignoreKeyNames is None else ignoreKeyNames
        objAJson = getattr(objA, toJsonMethodName)()
        objBJson = getattr(objB, toJsonMethodName)()
        differences = GeneralUtil.findDifferentFields(
            objAJson, objBJson, parentKey=parentKey, ignoreKeyNames=ignoreKeyNames
        )
        LOGGER.info(f"Differences: {differences}")
    return equal
