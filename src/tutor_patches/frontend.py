from pydantic import BaseModel, Field

from tutor_patches.slot import Slot


class FrontendPlugin(BaseModel):
    """
    Declarative frontend plugin configuration for Tutor.

    Example:
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

    package: str = Field(
        ...,
        description="NPM package name (e.g., '@myorg/frontend-plugin-foo')",
    )
    slots: list[Slot] = Field(
        default_factory=list,
        description="List of slot configurations",
    )
    local_path: str | None = Field(
        default=None,
        description="Local path for development (enables bind mount)",
    )

    def _build_slot_tuples(self) -> list[tuple[str, str, str]]:
        """Build all slot tuples for PLUGIN_SLOTS.add_items()."""
        items = []
        for slot in self.slots:
            items.extend(slot.to_tuples())
        return items

    def _build_import_statement(self) -> str:
        """Build the import statement for all components."""
        components = sorted(set(slot.component for slot in self.slots))
        return f"import {{ {', '.join(components)} }} from '{self.package}';"

    def _build_npm_install(self) -> str:
        """Build the npm install command."""
        return f"RUN npm install {self.package}"

    def register(self) -> None:
        """
        Register this plugin with Tutor hooks.

        This method:
        1. Adds slot configurations to PLUGIN_SLOTS
        2. Adds npm install patch for the package
        3. Adds import statement patch for components
        4. Optionally adds dev mount for local development
        """
        self._register_slots()
        self._register_npm_install()
        self._register_imports()
        if self.local_path:
            self._register_dev_mount()

    def _register_slots(self) -> None:
        """Register slot configurations with tutormfe."""
        from tutormfe.hooks import PLUGIN_SLOTS

        PLUGIN_SLOTS.add_items(self._build_slot_tuples())

    def _register_npm_install(self) -> None:
        """Register npm install patch."""
        from tutor import hooks

        hooks.Filters.ENV_PATCHES.add_item((
            "mfe-dockerfile-post-npm-install",
            self._build_npm_install(),
        ))

    def _register_imports(self) -> None:
        """Register component import patch."""
        from tutor import hooks

        hooks.Filters.ENV_PATCHES.add_item((
            "mfe-env-config-buildtime-imports",
            self._build_import_statement(),
        ))

    def _register_dev_mount(self) -> None:
        """Register bind mount for local development."""
        from tutor import hooks

        hooks.Filters.COMPOSE_MOUNTS.add_item((
            "mfe",
            self.local_path,
        ))
