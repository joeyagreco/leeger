from typing import Any, Optional

from leeger.util.CustomLogger import CustomLogger
from leeger.util.GeneralUtil import GeneralUtil


def modelEquals(
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
    equalityFunctionMap: Optional[dict[str, callable]] = None,
    equalityFunctionKwargsMap: Optional[dict[str, dict]] = None,
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
    equalityFunctionMap: maps the names of fields to a custom equality function that should be called for them*
    equalityFunctionKwargsMap: maps the names of fields to the kwargs that should be passed into their equalityFunctionMap

    *
    - equality functions should take at least 2 parameters (1 parameter for each field value).
    - equality functions should return a boolean.
    - equality functions should take **kwargs as the 3rd parameter.
    - equality functions will be passed the kwargs from equalityFunctionKwargsMap that match the field name (if given)
    """
    LOGGER = CustomLogger.getLogger()

    equalityFunctionMap = dict() if equalityFunctionMap is None else equalityFunctionMap
    equalityFunctionKwargsMap = (
        dict() if equalityFunctionKwargsMap is None else equalityFunctionKwargsMap
    )

    def isEqual(field: str, objA: Any, objB: Any) -> bool:
        if field in equalityFunctionMap:
            equalityFunction = equalityFunctionMap[field]
            # see if we should pass any kwargs
            kwargsToPass = (
                dict()
                if field not in equalityFunctionKwargsMap
                else equalityFunctionKwargsMap[field]
            )
            return equalityFunction(getattr(objA, field), getattr(objB, field), **kwargsToPass)
        return getattr(objA, field) == getattr(objB, field)

    equal = True
    for field in baseFields:
        equal = equal and isEqual(field, objA, objB)

    if not ignoreIdFields and idFields:
        for field in idFields:
            equal = equal and isEqual(field, objA, objB)

    if not equal and logDifferences:
        ignoreKeyNames = list() if ignoreKeyNames is None else ignoreKeyNames
        objAJson = getattr(objA, toJsonMethodName)()
        objBJson = getattr(objB, toJsonMethodName)()
        differences = GeneralUtil.findDifferentFields(
            objAJson, objBJson, parentKey=parentKey, ignoreKeyNames=ignoreKeyNames
        )
        LOGGER.info(f"Differences: {differences}")
    return equal
