import os

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
