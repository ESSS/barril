from docutils import nodes
from docutils.statemachine import ViewList
from sphinx.util import nested_parse_with_titles
from sphinx.util.docutils import SphinxDirective

from barril.units import UnitDatabase


class ListAllUnits(SphinxDirective):
    def run(self):
        rst = ViewList()
        unit_database = UnitDatabase.GetSingleton()
        source = "fakefile.rst"

        # Create the rst content
        for category in sorted(unit_database.IterCategories(), key=str.casefold):
            title = unit_database.GetCategoryInfo(category).caption.title()
            rst.append(f".. rubric:: {title}", source)
            rst.append(f"", source)

            for unit in sorted(
                unit_database.GetCategoryInfo(category).valid_units_set, key=str.casefold
            ):
                name = unit_database.unit_to_unit_info[unit].name
                rst.append(f'- ``"{unit}"`` ({name})', source)

            rst.append(f" ", source)

        # Create a node.
        node = nodes.section()
        node.document = self.state.document

        # Parse the rst.
        nested_parse_with_titles(self.state, rst, node)

        # And return the result.
        return node.children


def setup(app):
    app.add_directive("list_all_units", ListAllUnits)
    return {"version": "0.1", "parallel_read_safe": True, "parallel_write_safe": True}
