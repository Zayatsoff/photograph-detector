import os
import re

# Set the path of the Python file to be traversed
file_path = "C:/Users/Orange/miniconda3/envs/smile-detect/smile-detector - Copy/run.py"

# Set the file extension for the files to be deleted
extension = ".py"

# Set the list of directories to be excluded from the search
excluded_dirs = ["venv"]

# Set the list of files to be excluded from the search
excluded_files = ["__init__.py"]

# Set the list of local non-library imports in the file
local_imports = []

# Set the list of imported modules in the file
imported_modules = []

# Set the list of imported files in the file
imported_files = []

# Set the list of traversed files
traversed_files = []

# Set the list of deleted files
deleted_files = []

# Set the list of deleted directories
deleted_dirs = []


def get_local_imports(file_path):
    """Get the list of local non-library imports in a Python file."""
    # Open the file and read the contents
    with open(file_path, "r") as f:
        file_contents = f.read()

    # Use a regular expression to find all the local non-library imports in the file
    local_imports = re.findall(r"from (?!\.+)(.+?) import", file_contents)

    # Return the list of local non-library imports
    return local_imports


def get_imported_modules(file_path):
    """Get the list of imported modules in a Python file."""
    # Open the file and read the contents
    with open(file_path, "r") as f:
        file_contents = f.read()

    # Use a regular expression to find all the imported modules in the file
    imported_modules = re.findall(r"import (?!\.+)(.+?)[^\w]", file_contents)

    # Return the list of imported modules
    return imported_modules


def get_imported_files(file_path):
    """Get the list of imported files in a Python file."""
    # Open the file and read the contents
    with open(file_path, "r") as f:
        file_contents = f.read()

    # Use a regular expression to find all the imported files in the file
    imported_files = re.findall(r"from (?:\.+)(.+?) import", file_contents)

    # Return the list of imported files
    return imported_files


def delete_unnecessary_files(
    dir_path,
    extension,
    excluded_dirs,
    excluded_files,
    traversed_files,
    deleted_files,
    deleted_dirs,
):
    """Delete all unnecessary files in a directory and its subdirectories."""
    # Loop through the items in the directory
    for item in os.listdir(dir_path):
        # Ignore excluded directories
        if item in excluded_dirs:
            continue

        # Get the full path of the item
        item_path = os.path.join(dir_path, item)

        # If the item is a file, delete it if it has the specified extension and is not excluded
        if (
            os.path.isfile(item_path)
            and item.endswith(extension)
            and item not in excluded_files
        ):
            os.remove(item_path)
            deleted_files.append(item_path)
        # If the item is a directory, recursively delete unnecessary files in it
        elif os.path.isdir(item_path):
            delete_unnecessary_files(
                item_path,
                extension,
                excluded_dirs,
                excluded_files,
                traversed_files,
                deleted_files,
                deleted_dirs,
            )

    # If the directory is empty, delete it
    if not os.listdir(dir_path):
        os.rmdir(dir_path)
        deleted_dirs.append(dir_path)


# Get the local non-library imports, imported modules, and imported files in the file
local_imports = get_local_imports(file_path)
imported_modules = get_imported_modules(file_path)
imported_files = get_imported_files(file_path)

# Add the file to the list of traversed files
traversed_files.append(file_path)

# Loop through the local non-library imports
for local_import in local_imports:
    # Get the full path of the local import
    local_import_path = os.path.join(
        os.path.dirname(file_path), local_import + extension
    )

    # If the local import is not in the list of traversed files, traverse it and delete unnecessary files in it
    if local_import_path not in traversed_files:
        delete_unnecessary_files(
            os.path.dirname(local_import_path),
            extension,
            excluded_dirs,
            excluded_files,
            traversed_files,
            deleted_files,
            deleted_dirs,
        )
        traversed_files.append(local_import_path)

# Loop through the imported modules
for imported_module in imported_modules:
    # Get the imported files in the module
    module_imported_files = get_imported_files(imported_module)

    # Loop through the imported files in the module
    for module_imported_file in module_imported_files:
        # If the imported file is not in the list of traversed files, traverse it and delete unnecessary files in it
        if module_imported_file not in traversed_files:
            delete_unnecessary_files(
                os.path.dirname(module_imported_file),
                extension,
                excluded_dirs,
                excluded_files,
                traversed_files,
                deleted_files,
                deleted_dirs,
            )
            traversed_files.append(module_imported_file)

# Print the list of deleted files and directories
print("Deleted files:")
print(deleted_files)
print("Deleted directories:")
print(deleted_dirs)
