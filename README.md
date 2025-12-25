# Manifest builder for Talon

Automatically generates a manifest.json for your Talon packages (folders), discovering what actions, settings, and other features your package contributes and depends on, then resolving dependencies to specific package versions. Includes optional tools for generating version actions and installation instructions.

3 Scripts:
- `generate_manifest.py` - Generates `manifest.json`
- `generate_version_action.py` - Generates file `<my_package>_version.py` which includes Talon action `user.<my_package>_version()`
- `generate_install_block.py` - Outputs install instructions for your README to the terminal

## Installation

Clone this repository into your Talon user directory:

```sh
# mac and linux
cd ~/.talon/user

# windows
cd ~/AppData/Roaming/talon/user

git clone https://github.com/rokubop/manifest_builder
```

## Usage
```bash
cd manifest_builder
python generate_manifest.py ../my-package # generates or updates ../my-package/manifest.json
python generate_version_action.py ../my-package # generates ../my-package/my_package_version.py
python generate_install_block.py ../my-package # outputs install instructions

# or multiple packages at once
python generate_manifest.py ../package1 ../package2
```

## How Manifest Generation Works

Parses Python files using AST to detect Talon actions, settings, tags, lists, modes, scopes, and captures you contribute or depend on. Scans user directory to find all other packages with manifests to build an index of available packages. Maps your imported actions/settings to specific packages and their versions. Creates or updates manifest.json with all discovered information, preserving your manual edits to fields like name, description, etc.

## Example Manifest Output

```json
{
  "name": "my_package",
  "title": "My Package",
  "description": "A brief description of what the package does",
  "version": "1.0.0",
  "namespace": "user.my_package",
  "github": "https://github.com/user/my-package",
  "preview": "",
  "author": "Your Name",
  "tags": ["productivity", "editing"],
  "dependencies": {
    "ui_elements": "0.10.0"
  },
  "devDependencies": {},
  "contributes": {
    "actions": ["user.my_package_action"],
    "settings": ["user.my_package_setting"]
  },
  "depends": {
    "actions": ["user.ui_elements_show"]
  },
  "_generator": "manifest_builder",
  "_generatorVersion": "1.0.0"
}
```

### Manifest Fields

| Field | Description |
|-------|-------------|
| name | Package identifier (defaults to folder name, preserved on updates) |
| title | Human-readable package title |
| description | Brief description of package functionality |
| version | Semantic version number |
| namespace | Naming prefix for all package contributions (e.g. `user.ui_elements` means all actions should be `user.ui_elements_*`) |
| github | GitHub repository URL |
| preview | Preview image URL |
| author | Package author name |
| tags | Category tags for the package |
| dependencies | Required packages with versions (auto-generated) |
| devDependencies | Dev-only dependencies (manually move items here from `dependencies` if only needed for testing/development) |
| contributes | Actions/settings/etc. this package provides (auto-generated) |
| depends | Actions/settings/etc. this package uses (auto-generated) |
| _generator | Tool that generated this manifest |
| _generatorVersion | Version of the generator tool |

Most fields are preserved across regenerations, but `contributes`, `depends`, and `dependencies` are auto-generated each time.