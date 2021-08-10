"""Builtin domains."""
from mold import Domain, hook

module = 'mold_builtin'

python = Domain(module, 'Python', 'begin developing a Python project')
hook.add_domain(python)
