from subprocess import run


class TestCLI:
    def test_config_list(self):
        pc = run(['mold', 'config', 'list'])
        assert pc.returncode == 0

    def test_config_show(self):
        pc = run(['mold', 'config', 'show', 'python-library'])
        assert pc.returncode == 0

    def test_prefill_show(self):
        pc = run(['mold', 'prefill', 'show'])
        assert pc.returncode == 0
