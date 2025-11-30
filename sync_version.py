#!/usr/bin/env python3
"""Sync version and dependencies across project files."""

import re
import sys

def get_version_from_helper():
    """Extract version from helper.py."""
    with open('src/helper.py', 'r') as f:
        content = f.read()
        match = re.search(r'VERSION = "v([0-9.]+(?:-[a-z0-9]+)?)"', content)
        if match:
            return match.group(1)
    raise ValueError("Version not found in helper.py")

def parse_requirements():
    """Parse requirements.txt and return dict of dependencies."""
    deps = {}
    with open('src/requirements.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Handle conditional dependencies
                if ';' in line:
                    pkg, condition = line.split(';', 1)
                    pkg = pkg.strip()
                    condition = condition.strip()
                else:
                    pkg = line
                    condition = None
                
                # Parse package name and version
                if '==' in pkg:
                    name, version = pkg.split('==', 1)
                    deps[name.strip()] = (version.strip(), condition)
    return deps

def update_setup_py(version, deps):
    """Update setup.py with version and dependencies."""
    with open('setup.py', 'r') as f:
        content = f.read()
    
    # Update version
    content = re.sub(r'version="[^"]*"', f'version="{version}"', content)
    
    # Build install_requires list
    install_requires = []
    for name, (ver, condition) in deps.items():
        if name == 'pyinstaller':  # Skip build-only deps
            continue
        if condition:
            # Replace double quotes with single quotes in condition
            condition = condition.replace('"', "'")
            dep_str = f'"{name}>={ver}; {condition}"'
        else:
            dep_str = f'"{name}>={ver}"'
        install_requires.append(dep_str)
    
    # Update install_requires
    install_requires_str = ',\n        '.join(install_requires)
    content = re.sub(
        r'install_requires=\[.*?\]',
        f'install_requires=[\n        {install_requires_str},\n    ]',
        content,
        flags=re.DOTALL
    )
    
    with open('setup.py', 'w') as f:
        f.write(content)
    print(f"✓ Updated setup.py to version {version}")

def update_pkgbuild(version):
    """Update PKGBUILD with version."""
    with open('PKGBUILD', 'r') as f:
        content = f.read()
    
    content = re.sub(r'pkgver=[0-9.]+', f'pkgver={version}', content)
    
    with open('PKGBUILD', 'w') as f:
        f.write(content)
    print(f"✓ Updated PKGBUILD to version {version}")

def main():
    try:
        version = get_version_from_helper()
        print(f"Version from helper.py: {version}")
        
        deps = parse_requirements()
        print(f"Dependencies from requirements.txt: {len(deps)} packages")
        
        update_setup_py(version, deps)
        update_pkgbuild(version)
        
        print("\n✓ All files synced successfully!")
        
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
