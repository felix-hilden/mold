import mold
from mold.cli import load_entry_points


class TestPackage:
    def test(self):
        assert mold.__version__

    def test_load_plugins(self):
        load_entry_points()
