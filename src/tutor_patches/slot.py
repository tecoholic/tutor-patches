from pydantic import BaseModel, Field, field_validator

from tutor_patches.types import Operation, PluginType
from tutor_patches.validation import validate_mfe


class Slot(BaseModel):
    """Configuration for a frontend plugin slot."""

    mfe: str = Field(
        ...,
        description="Target MFE name (e.g., 'learner-dashboard') or 'all' for all MFEs",
    )
    slot_name: str = Field(
        ...,
        description="Name of the slot to target (e.g., 'course_list_slot')",
    )
    component: str = Field(
        ...,
        description="Name of the React component to render",
    )
    operation: Operation = Field(
        default=Operation.INSERT,
        description="Plugin operation type",
    )
    plugin_type: PluginType = Field(
        default=PluginType.DIRECT,
        description="Plugin implementation type",
    )
    priority: int = Field(
        default=50,
        ge=0,
        description="Loading priority (higher loads later)",
    )
    hide_default: bool = Field(
        default=False,
        description="Whether to hide the default slot contents",
    )

    @field_validator("mfe")
    @classmethod
    def validate_mfe_name(cls, v: str) -> str:
        return validate_mfe(v)

    def to_jsx(self) -> str:
        """Generate JSX configuration string for this slot."""
        return f"""{{
  op: PLUGIN_OPERATIONS.{self.operation.value},
  widget: {{
    id: '{self.slot_name}_{self.component}',
    type: {self.plugin_type.value},
    priority: {self.priority},
    RenderWidget: {self.component},
  }},
}}"""

    def to_hide_jsx(self) -> str:
        """Generate JSX to hide the default slot contents."""
        return """{
  op: PLUGIN_OPERATIONS.Hide,
  widgetId: 'default_contents',
}"""

    def to_tuples(self) -> list[tuple[str, str, str]]:
        """Generate tuples for PLUGIN_SLOTS.add_items()."""
        items = []
        if self.hide_default:
            items.append((self.mfe, self.slot_name, self.to_hide_jsx()))
        items.append((self.mfe, self.slot_name, self.to_jsx()))
        return items
