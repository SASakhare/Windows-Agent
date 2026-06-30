import inspect
from typing import Any, Dict, Type


def build_tool_schema(tool_class: Type) -> Dict[str, Any]:
    """
    Generate a tool schema from a class using its public methods,
    type hints, default values, and docstrings.

    Args:
        tool_class: Tool class (not an instance).

    Returns:
        Dictionary containing the tool schema.
    """

    def build_action_schema(func):
        signature = inspect.signature(func)

        parameters = {}

        for name, param in signature.parameters.items():

            # Ignore internal parameters
            if name in ("self", "action"):
                continue

            if param.kind == inspect.Parameter.VAR_KEYWORD:
                continue

            annotation = (
                param.annotation.__name__
                if param.annotation != inspect._empty
                and hasattr(param.annotation, "__name__")
                else (
                    str(param.annotation)
                    if param.annotation != inspect._empty
                    else "Any"
                )
            )

            parameters[name] = {
                "type": annotation,
                "required": param.default == inspect._empty,
                "default": (None if param.default == inspect._empty else param.default),
            }

        return_annotation = func.__annotations__.get("return", None)

        if hasattr(return_annotation, "__name__"):
            return_annotation = return_annotation.__name__
        elif return_annotation is None:
            return_annotation = "None"
        else:
            return_annotation = str(return_annotation)

        return {
            "name": func.__name__,
            "description": inspect.getdoc(func) or "",
            "parameters": parameters,
            "returns": return_annotation,
        }

    schema = {
        "tool": tool_class.__name__,
        "description": inspect.getdoc(tool_class) or "",
        "actions": [],
    }

    for name, func in inspect.getmembers(
        tool_class,
        predicate=inspect.isfunction,
    ):

        # Ignore private/internal methods
        if name.startswith("_"):
            continue

        # Ignore dispatcher
        if name == "execute":
            continue

        schema["actions"].append(build_action_schema(func))

    return schema
