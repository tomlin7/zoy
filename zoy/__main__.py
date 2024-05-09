import sys

from .zoy import count_lines_files_dirs

if __name__ == "__main__":
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = input("Enter the directory path: ")
    
    total_lines, file_count, dir_count, tree = count_lines_files_dirs(directory_path)

    print("Project Structure: ")
    for line in tree:
        print(line)

    print("\n=========================================")

    print(f"\nTotal Python files: {file_count}")
    print(f"Total lines in Python files: {total_lines}")
    print(f"Total directories: {dir_count}")
