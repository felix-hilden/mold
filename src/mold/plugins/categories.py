"""Builtin categories."""
from mold import Category
from .domains import module

gitignore = Category(module, 'gitignore', '.gitignore file for git')
license_ = Category(module, 'license', 'license applied to the project')
source = Category(module, 'source', 'project source code')
