import os
import tempfile
import subprocess

def is_hidden(filepath):
    name = os.path.basename(filepath)
    return name.startswith('.') or has_hidden_attribute(filepath)

def has_hidden_attribute(filepath):
    try:
        import ctypes
        attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
        assert attrs != -1
        result = bool(attrs & 2)
    except (AttributeError, AssertionError):
        result = False
    return result

def write_dir_structure(root_dir, output_file, prefix='', skip_dirs=None, included_dirs=set()):
    if skip_dirs is None:
        skip_dirs = {'.git', 'node_modules', '.vscode', 'venv', 'env', '__pycache__', 'dist', 'build'}

    try:
        files_and_dirs = os.listdir(root_dir)
    except FileNotFoundError:
        output_file.write(f"Error: Directory '{root_dir}' was not found.\n")
        return
    except PermissionError:
        output_file.write(f"Error: No permission to access the directory '{root_dir}'.\n")
        return

    files_and_dirs.sort()
    for index, name in enumerate(files_and_dirs):
        path = os.path.join(root_dir, name)
        is_last = index == len(files_and_dirs) - 1
        hidden_prefix = "* " if is_hidden(path) else ""
        folder_indicator = "/" if os.path.isdir(path) else ""

        connector = "└── " if is_last else "├── "
        output_file.write(prefix + connector + hidden_prefix + name + folder_indicator + "\n")

        if os.path.isdir(path) and (name not in skip_dirs or name in included_dirs):
            extra_prefix = '    ' if is_last else '│   '
            write_dir_structure(path, output_file, prefix + extra_prefix, skip_dirs, included_dirs)

def print_help():
    print(" ")
    print("Commands:")
    print("  exit: Quit the program")
    print("  help: Show this help message")
    print("  include [dir]: Include a directory to show its contents")
    print("  exclude [dir]: Exclude a directory from showing its contents")
    print("  list: List current inclusions and exclusions")

    print(" ")
    print(" ")
    print("* hidden directiry")
    print(" ")

excluded_dirs = {'.git', 'node_modules'}
included_dirs = set()

while True:
    command = input("Enter command or path (type 'help' for commands): ").strip()

    if command.lower() == 'exit':
        break
    elif command.lower() == 'help':
        print_help()
    elif command.lower().startswith('exclude '):
        dir_name = command[8:].strip()
        excluded_dirs.add(dir_name)
        included_dirs.discard(dir_name)
        print(f"Excluded '{dir_name}'")
    elif command.lower().startswith('include '):
        dir_name = command[8:].strip()
        included_dirs.add(dir_name)
        excluded_dirs.discard(dir_name)
        print(f"Included '{dir_name}'")
    elif command.lower() == 'list':
        print("Currently included directories:")
        for dir_name in included_dirs:
            print(f"  {dir_name}")
        print("Currently excluded directories:")
        for dir_name in excluded_dirs:
            print(f"  {dir_name}")
    else:
        root_dir = command
        scheme_file_name = os.path.basename(root_dir) + "Scheme.txt"
        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding='utf-8', suffix=".txt", prefix=scheme_file_name) as temp_file:
            temp_file.write(root_dir + "/\n")
            write_dir_structure(root_dir, temp_file, skip_dirs=excluded_dirs, included_dirs=included_dirs)
            temp_file_path = temp_file.name

        subprocess.Popen(["notepad", temp_file_path])
