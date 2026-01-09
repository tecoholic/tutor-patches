# tutor-patches

Declarative frontend plugin configuration for Tutor.

This library simplifies adding frontend plugins to Open edX deployments via Tutor by providing a clean Python API that handles all the boilerplate (slot configuration, npm installation, imports).

> [!CAUTION]
> The code in this library was generated using LLMs as a Proof of Concept and not intended for general consumption.

## Installation

```bash
pip install git+https://github.com/tecoholic/tutor-patches.git
```

## Usage

Use this library directly inside your Tutor plugin:

```python
# my_tutor_plugin/plugin.py
from tutor_patches import FrontendPlugin, Slot, Operation

FrontendPlugin(
    package="@myorg/frontend-plugin-dashboard",
    slots=[
        Slot(
            mfe="learner-dashboard",
            slot_name="course_list_slot",
            component="CustomCourseList",
            hide_default=True,  # Hide the default component
        ),
        Slot(
            mfe="all",
            slot_name="footer_slot",
            component="CustomFooter",
            priority=10,
        ),
    ],
).register()
```

This single declaration will:
1. Register slot configurations with `tutormfe.hooks.PLUGIN_SLOTS`
2. Add npm install patch for your package
3. Add import statement for your components

## API

### `Slot`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mfe` | `str` | required | Target MFE (e.g., `"learner-dashboard"`) or `"all"` |
| `slot_name` | `str` | required | Name of the slot to target |
| `component` | `str` | required | React component name to render |
| `operation` | `Operation` | `INSERT` | `INSERT` or `HIDE` |
| `plugin_type` | `PluginType` | `DIRECT` | `DIRECT` or `IFRAME` |
| `priority` | `int` | `50` | Loading priority (higher loads later) |
| `hide_default` | `bool` | `False` | Hide the default slot contents |

### `FrontendPlugin`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `package` | `str` | required | NPM package name |
| `slots` | `list[Slot]` | `[]` | List of slot configurations |
| `local_path` | `str \| None` | `None` | Local path for dev bind mount |

## Local Development

For local development, provide `local_path` to enable bind mounting:

```python
FrontendPlugin(
    package="@myorg/frontend-plugin-dashboard",
    local_path="/home/user/dev/frontend-plugin-dashboard",
    slots=[...],
).register()
```

## Known MFEs

The library will warn (but not error) if you use an unknown MFE name:

- `account`, `authn`, `communications`, `course-authoring`
- `discussions`, `gradebook`, `learner-dashboard`, `learning`
- `ora-grading`, `profile`
- `all` (applies to all MFEs with the slot)
