import pytest

from .__main__ import count_lines_files_dirs

def test_addition():
    line, _, _, _ = count_lines_files_dirs(".")
    assert line == 61

if __name__ == "__main__":
    pytest.main()
