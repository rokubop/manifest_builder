# Manifest builder for Talon folder(s)

Manifest builder generates a `manifest.json` file for your specified folder(s) by discovering talons actions, modes, tags, lists, and other talon entities that the folder(s) contributes and depends on, using AST parsing.

# Usage

1. Copy `manifest_targets.example.txt` to `manifest_targets.txt`.
2. Edit `manifest_targets.txt` to include the directories where manifests should be generated. Directories should be relative to the `manifest_builder.py` script location.
3. Run: `python manifest_builder.py` to generate `manifest.json` in the specified target directories. If a `manifest.json` already exists, it will be updated with the new information.