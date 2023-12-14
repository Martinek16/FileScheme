# FileScheme

## Description

This project includes a Python script that enables visualization of a directory's structure in a tree-like format. The script can display all directories and files, including hidden elements, and allows the user to exclude or include specific directories from the display. Additionally, special directories like `.git` and `node_modules` are defaulted to be collapsed to reduce display clutter.

## Features

- Display of directory structure in a tree-like format.
- Support for displaying hidden files and directories.
- Option to exclude or include specific directories from the display.
- Special directories like `.git` are collapsed by default.
- Interactive user interface through the console.

## How to Use

1. Run the script in a Python interpreter.
2. Enter the path to the directory you want to scan or use one of the commands (`help`, `exit`, `include [dir]`, `exclude [dir]`, `list`).
3. Review the displayed directory structure in the opened text editor (e.g., Notepad).

## Commands

- `exit`: Exit the program.
- `help`: Display a list of commands.
- `include [dir]`: Include a directory to show its contents.
- `exclude [dir]`: Exclude a directory from the display.
- `list`: List of current inclusions and exclusions.

## License

The project is available under the [MIT License](LICENSE).

