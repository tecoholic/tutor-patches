"""
tutor-patches: Declarative frontend plugin configuration for Tutor.

Example:
    from tutor_patches import FrontendPlugin, Slot, Operation

    FrontendPlugin(
        package="@myorg/frontend-plugin-dashboard",
        slots=[
            Slot(
                mfe="learner-dashboard",
                slot_name="course_list_slot",
                component="CustomCourseList",
                hide_default=True,
            ),
        ],
    ).register()
"""

from tutor_patches.frontend import FrontendPlugin
from tutor_patches.slot import Slot
from tutor_patches.types import Operation, PluginType

__all__ = [
    "FrontendPlugin",
    "Operation",
    "PluginType",
    "Slot",
]
