from pytest import raises
from mold.doc import render_doc, render_docs


class TestDoc:
    def test_render_domain(self):
        render_doc('mold.plugins.domains.python')

    def test_render_interface(self):
        render_doc('mold.plugins.face.build.interface')

    def test_render_category(self):
        render_doc('mold.plugins.categories.gitignore')

    def test_render_tool(self):
        render_doc('mold.plugins.tools.github.tool')

    def test_invalid_import_location(self):
        with raises(ValueError):
            render_doc('mold.this.does.not.exist')

    def test_invalid_import_type(self):
        with raises(ValueError):
            render_doc('mold.__version__')

    def test_render_docs(self):
        render_docs(
            'intro',
            ['mold.plugins.domains.python'],
            ['mold.plugins.tools.github.tool'],
            ['mold.plugins.categories.gitignore'],
            ['mold.plugins.face.build.interface'],
        )
