from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Config:
    def buildtime_imports(self, value):
        return ("mfe-env-config-buildtime-imports", value)


class Env:
    def __init__(self) -> None:
        self.config = Config()

class Dockerfile:
    def __init__(self) -> None:
        self._post_npm_installs = []

    def post_npm_install(self, command: str):
        self._post_npm_installs.append

class Patches:
    def __init__(self) -> None:
        self.dockerfile = Dockerfile()
        self.env = Env()


# from tutor_patches.mfe import Patches as MFEPatches
#
# MFE = MFEPatches()
#
# MFE.dockerfile.post_npm_install("RUN npm install react-loader-spinner")
# MFE.env.config.buildtime_imports("""
# import { FidgetSpinner } from 'react-loader-spinner';
# """)
class PluginOperations(str, Enum):
    Insert = 'PLUGIN_OPERATIONS.Insert'
    Hide = 'PLUGIN_OPERATIONS.Hide'


class PluginType(str, Enum):
    Direct = 'DIRECT_PLUGIN'


class Widget(BaseModel):
    id: str
    type: PluginType
    RenderWidget: str  # We should be able to validate that this was imported before usage

class SlotDefinition(BaseModel):
    op: PluginOperations
    widgetId: Optional[str] = None
    widget: Widget

class HideDefaultConteents:
    def __init__(self) -> None:
        pass


class SlotItem:
    def __init__(self, mfe_name: str, slot_id: str, definition: SlotDefinition|HideDefaultConteents) -> None:
        pass


SlotItem(
    "learner-dashboard",
    "org.openedx.frontend.learner_dashboard.no_courses.view.v1",
    HideDefaultConteents()
)
SlotItem(
    "learner-dashboard",
    "org.openedx.frontend.learner_dashboard.no_courses.view.v1",
    SlotDefinition(
        op=PluginOperations.Insert,
        widget=Widget(
            id='my-id',
            type=PluginType.Direct,
            RenderWidget='HEE'
        )
    )
)
