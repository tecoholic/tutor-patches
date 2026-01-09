from enum import Enum


class Operation(str, Enum):
    """Plugin operations for frontend slots."""

    INSERT = "Insert"
    HIDE = "Hide"


class PluginType(str, Enum):
    """Plugin implementation type."""

    DIRECT = "DIRECT_PLUGIN"
    IFRAME = "IFRAME_PLUGIN"
