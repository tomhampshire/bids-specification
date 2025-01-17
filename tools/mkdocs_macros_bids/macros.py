"""Functions used by the macros mkdocs plugin."""
import os
import sys

from bidsschematools import render, schema, utils

code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(code_path)

from examplecode import example


def _get_source_path(level=1):
    """ Detect the path of the file we are rendering a macro in.

    This (ab)uses the Python call stack to find its way to the Jinja2 function
    that is calling the macro. From there, it looks at Jinja2's Context object,
    which contains all the variables available to the Markdown snippet that is
    calling the macro.

    One variable provided by mkdocs-macros is called ``page``, which includes a
    ``file`` attribute that would allow us to insert the page name into the text
    of the page, or in this case, pass it as a variable. The ``file`` attribute
    has a ``src_path`` attribute of its own that is a path relative to the ``src/``
    directory.

    The level parameter indicates how many steps above the calling function Jinja2
    is. Currently it's always 1, but refactors may justify passing a larger number.

    This allows us to use

    ```{markdown}
    {{ MACRO__make_glossary() }}
    ```

    instead of:

    ```{markdown}
    {{ MACRO__make_glossary(page.file.src_path) }}
    ```

    Why are we doing all this? We need to render links that are defined in the schema
    relative to the source tree as paths relative to the Markdown file they're being
    rendered in. So [SPEC_ROOT/02-common-principles.md](Common principles) becomes
    [./02-common-principles.md](Common principles) or
    [../02-common-principles.md](Common principles), depending on which file it
    appears in.

    If a future maintainer decides that this is terrible, or a bug can't be fixed,
    just go back to explicitly using the ``page.file`` variable throughout the macros.
    """
    import inspect

    # currentframe = _get_source_path()
    # caller = the macro calling this function, e.g. make_glossary()
    caller = inspect.currentframe().f_back
    # We need to go one level higher to find Jinja2
    for _ in range(level):
        caller = caller.f_back
    # Jinja2 equivalent: {{ page.file.src_path }}
    return caller.f_locals["_Context__self"]["page"].file.src_path


def make_filename_template(**kwargs):
    """Generate a filename template snippet from the schema, based on specific
    filters.

    Parameters
    ----------
    kwargs : dict
        Keyword arguments used to filter the schema.
        Example kwargs that may be used include: "suffixes", "datatypes",
        "extensions".

    Returns
    -------
    codeblock : str
        A multiline string containing the filename templates for file types
        in the schema, after filtering.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    codeblock = render.make_filename_template(schema_obj, **kwargs)
    return codeblock


def make_entity_table(**kwargs):
    """Generate an entity table from the schema, based on specific filters.

    Parameters
    ----------
    kwargs : dict
        Keyword arguments used to filter the schema.
        Example kwargs that may be used include: "suffixes", "datatypes",
        "extensions".

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding entity table for
        a subset of the schema.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_entity_table(schema_obj, **kwargs)
    return table


def make_entity_definitions():
    """Generate definitions and other relevant information for entities in the
    specification.

    Returns
    -------
    text : str
        A multiline string containing descriptions and some formatting
        information about the entities in the schema.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    text = render.make_entity_definitions(schema_obj)
    return text


def make_glossary(src_path=None):
    """Generate glossary.

    Parameters
    ----------
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    text : str
        A multiline string containing descriptions and some formatting
        information about the entities in the schema.
    """
    if src_path is None:
        src_path = _get_source_path()
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    text = render.make_glossary(schema_obj, src_path=src_path)
    return text


def make_suffix_table(suffixes, src_path=None):
    """Generate a markdown table of suffix information.

    Parameters
    ----------
    suffixes : list of str
        A list of the suffixes to include in the table.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    if src_path is None:
        src_path = _get_source_path()
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_suffix_table(schema_obj, suffixes, src_path=src_path)
    return table


def make_metadata_table(field_info, src_path=None):
    """Generate a markdown table of metadata field information.

    Parameters
    ----------
    field_names : dict
        A list of the field names.
        Field names correspond to filenames in the "metadata" directory of the
        schema.
        Until requirement levels can be codified in the schema,
        this argument will be dictionary, with the field names as keys and
        the requirement levels as values.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    if src_path is None:
        src_path = _get_source_path()
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_metadata_table(schema_obj, field_info, src_path=src_path)
    return table


def make_subobject_table(object_tuple, field_info, src_path=None):
    """Generate a markdown table of a metadata object's field information.

    Parameters
    ----------
    object_tuple : tuple of string
        A tuple pointing to the object to render.
    field_names : dict
        A list of the field names.
        Field names correspond to filenames in the "metadata" directory of the
        schema.
        Until requirement levels can be codified in the schema,
        this argument will be dictionary, with the field names as keys and
        the requirement levels as values.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    if src_path is None:
        src_path = _get_source_path()

    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_subobject_table(schema_obj, object_tuple, field_info, src_path=src_path)
    return table


def make_columns_table(column_info, src_path=None):
    """Generate a markdown table of TSV column information.

    Parameters
    ----------
    column_info : dict
        A list of the column names.
        Column names correspond to filenames in the "columns" directory of the
        schema.
        Until requirement levels can be codified in the schema,
        this argument will be a dictionary, with the column names as keys and
        the requirement levels as values.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested columns.
    """
    if src_path is None:
        src_path = _get_source_path()
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_columns_table(schema_obj, column_info, src_path=src_path)
    return table


def make_filetree_example(filetree_info, use_pipe=True):
    """Generate a filetree snippet from example content.

    Parameters
    ----------
    filetree_info : dict
        Dictionary to represent the directory content.
    use_pipe : bool
        Set to ``False`` to avoid using pdf unfriendly pipes: "│ └─ ├─"

    Returns
    -------
    tree : str
        A multiline string containing the filetree example.
    """
    tree = example.DirectoryTree(filetree_info, use_pipe)
    return tree.generate()
