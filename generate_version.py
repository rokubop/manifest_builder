import json
import os
import sys

"""
Generate a Talon action that exposes package version from manifest.json.

Usage: python generate_version_talon_action.py <package_directory>
Example: python generate_version_talon_action.py ../my-package
"""

def generate_version_action(package_dir: str) -> None:
    """Generate version action file for a package"""
    full_package_dir = os.path.abspath(package_dir)

    if not os.path.isdir(full_package_dir):
        print(f"Error: Directory not found: {full_package_dir}")
        sys.exit(1)

    # Read manifest.json
    manifest_path = os.path.join(full_package_dir, 'manifest.json')
    if not os.path.exists(manifest_path):
        print(f"Error: manifest.json not found in {full_package_dir}")
        print("Run manifest_builder.py first to generate a manifest.")
        sys.exit(1)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    namespace = manifest.get('namespace', 'package')
    package_name = manifest.get('name', os.path.basename(full_package_dir))
    
    # Check if file already exists
    version_file_path = os.path.join(full_package_dir, f'{namespace}_version.py')
    if os.path.exists(version_file_path):
        print(f"⚠ Warning: {version_file_path} already exists")
        response = input("Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            sys.exit(0)

    # Generate the version action file
    version_file_content = f'''"""Auto-generated version action for {package_name}"""
import json
import os
from talon import Module

mod = Module()

def get_version():
    """Returns (major, minor, patch) from manifest.json"""
    manifest_path = os.path.join(os.path.dirname(__file__), 'manifest.json')
    with open(manifest_path, 'r', encoding='utf-8') as f:
        version_str = json.load(f)['version']
    return tuple(map(int, version_str.split('.')))

@mod.action_class
class Actions:
    def {namespace}_version() -> tuple[int, int, int]:
        """Returns the package version as (major, minor, patch)"""
        return get_version()
'''
    
    display_path = version_file_path.replace('\\', '/')
    print(f"\nWill create: {display_path}")
    print(f"Action: actions.user.{namespace}_version()")
    print(f"\nThis will NOT modify any existing files (only creates {namespace}_version.py)")
    
    try:
        response = input("\nContinue? (Y/n): ").strip().lower()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
    
    if response == 'n':
        print("Cancelled.")
        sys.exit(0)

    # Write the version file
    with open(version_file_path, 'w', encoding='utf-8') as f:
        f.write(version_file_content)

    print(f"\n✓ Generated: {version_file_path}")
    print(f"  Action: actions.user.{namespace}_version()")
    print(f"\nUsage in other packages:")
    print(f"  version = actions.user.{namespace}_version()")
    print(f"  print(version)  # (1, 0, 0)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_version_talon_action.py <directory>")
        print("Example: python generate_version_talon_action.py ../my-package")
        sys.exit(1)

    package_dir = sys.argv[1]
    generate_version_action(package_dir)
