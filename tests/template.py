import pytest
from pathlib import Path
from mold import template


class TestTemplate:
    def test_undeclared_vars(self):
        t = '{{ var }} ordinary text {% for item in collection %}{{ item }}{% endfor%}'
        assert template.undeclared_vars(t) == {'var', 'collection'}

    def test_render(self):
        t = '{{ v }} {% for i in c %}{{ i }}{% endfor %}'
        assert template.render(t, {'v': 0, 'c': [1, 2, 3]}) == '0 123'

    def test_write(self, tmpdir):
        file = Path(tmpdir) / 'test'
        template.write(file, 'content')

    def test_write_nonempty_fails(self, tmpdir):
        file = Path(tmpdir) / 'test'
        file.touch()
        with pytest.raises(FileExistsError):
            template.write(file, 'content')
