import pytest
from pathlib import Path
from unittest.mock import patch
from mold import config, hook, cli


class TestConfig:
    def test_read_config(self):
        config.read_config('mold-plugin')

    def test_write_user_config(self, tmpdir):
        conf = config.StrConfig('name', 'domain', list('str'))
        with patch('mold.config.user_configs', Path(tmpdir)):
            config.write_config(conf)

    def test_overwrite_builtin_config_raises(self, tmpdir):
        conf = config.StrConfig('mold-plugin', 'domain', list('str'))
        with patch('mold.config.user_configs', Path(tmpdir)):
            with pytest.raises(FileExistsError):
                config.write_config(conf)

    def test_delete_config(self, tmpdir):
        name = 'name'
        conf = config.StrConfig(name, 'domain', list('str'))
        with patch('mold.config.user_configs', Path(tmpdir)):
            config.write_config(conf)
            config.read_config(name)
            config.delete_config(name)
            with pytest.raises(FileNotFoundError):
                config.read_config(name)

    def test_read_all_configs(self):
        config.read_all_configs()

    def test_concretise_abstract_config(self):
        cli.load_entry_points()
        domains = hook._domains
        conf = config.StrConfig('name', repr(domains[0]), [repr(domains[0].tools[0])])
        concrete = config.concretise_config(conf, domains)
        abstract = config.abstract_config(concrete)
        assert conf == abstract
