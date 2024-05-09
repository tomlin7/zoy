import pytest

from zoy import count_lines_files_dirs

def test_addition():
    line, _, _, _ = count_lines_files_dirs(".")
    assert line == 130

if __name__ == "__main__":
    pytest.main()
