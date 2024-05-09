import os
import sys
import tomllib

from pytermgui import Container, Label, boxes, pretty, SizePolicy

def count_lines_files_dirs(directory):
    total_lines = 0
    file_count = 0
    dir_count = 0
    tree = []

    def build_tree(path, level=0):
        nonlocal total_lines, file_count, dir_count

        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)

            if entry.startswith('.') or entry in ('.git', '__pycache__', '.pytest_cache', 'venv'):
                continue

            if os.path.isdir(entry_path):
                dir_count += 1
                tree.append("  " * level + "📂 " + entry)
                build_tree(entry_path, level + 1)

            elif entry.endswith(".py"):
                file_count += 1
                with open(entry_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                tree.append("  " * level + "📄 " + entry)

    build_tree(directory)
    return total_lines, file_count, dir_count, tree

def do(fn):
    try:
        fn()
    except Exception as e:
        pass

def main():
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = input("Enter the directory path: ")
    
    try:
        directory_path = os.path.abspath(directory_path)
        if not os.path.exists(directory_path):
            raise Exception(f"Directory does not exist: {directory_path}")
    except Exception as e:
        c = Container(f"[red bold]Error:[/] {e}", box="EMPTY")
        for line in c.get_lines():
            print(line)
        return
    
    total_lines, file_count, dir_count, tree = count_lines_files_dirs(directory_path)

    pyproject_data = {}
    pyproject_path = os.path.join(directory_path, 'pyproject.toml')
    if os.path.exists(pyproject_path):
        with open(pyproject_path, 'rb') as f:
            pyproject_data = tomllib.load(f)

    container = Container(box="EMPTY")
    container += Container(f"[bold !gradient(56)]{os.path.basename(directory_path)}", box=boxes.HEAVY)

    items = ["[primary bold]Project Structure[/]"]
    for line in tree:
        items.append(Label(line, parent_align=0))

    container +=  Container(*items, box=boxes.SINGLE_VERTICAL, static_width=40)

    items = [
        f"[primary bold]Total Lines of Code:[/] {total_lines}",
        f"[primary bold]Total Files:[/] {file_count}",
        f"[primary bold]Total Directories:[/] {dir_count}"
    ]

    container += Container(*items, box=boxes.DOUBLE_VERTICAL)

    if pyproject_data:
        items = []
        def add(val: dict):
            for key, value in val.items():
                if isinstance(value, dict):
                    add(value)
                    continue

                match key:
                    case "name":
                        style = f"[bold !gradient(50)]"
                    case "description":
                        style = f"[lightblue bold]"
                    case "version":
                        style = f"[italic !gradient(50)]"
                    case "license":
                        style = f"[bold primary]"
                    case "authors":
                        style = f"[italic lightblue]"
                        items.append(Label(f"[grey]{key}[/]: {style}{', '.join(value)}", parent_align=0))
                        continue
                    case _:
                        continue
                
                items.append(Label(f"[grey]{key}[/]: {style}{value}", parent_align=0))
        add(pyproject_data)
        container += Container(*items, box=boxes.SINGLE_VERTICAL)

    for line in container.get_lines():
        print(line)
