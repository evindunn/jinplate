#!/usr/bin/env python3

import importlib
import pathlib

import click
import jinja2

from jinplate.plugins.loader import DataLoader


def _render_template(template_file, extensions, **kwargs):
    """
    Attempts to lazy-load ansible and use it to render template_file with kwargs as
    variable input. If ansible is not available, uses plain jinja2
    :param template_file: Path to the template file to render
    :param extensions: Jinja2 extensions to load
    :param kwargs: K/V arguments for the template
    :return: The rendered template
    """
    template_path = pathlib.Path(template_file).resolve()
    try:
        ansible_template = importlib.import_module('ansible.template')
        ansible_dataloader = importlib.import_module('ansible.parsing.dataloader')
        loader = ansible_dataloader.DataLoader()
        loader.set_basedir(template_path.parent)
        templar = ansible_template.Templar(loader=loader, variables=kwargs)
        return templar.template(template_path.read_text(encoding="utf-8"))
    except ImportError:
        jenv = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_path.parent),
            extensions=extensions,
        )
        template = jenv.get_template(template_path.name)
        return template.render(kwargs)


@click.command("jinplate")
@click.option("--jinja-ext", type=str, default=None)
@click.argument("template_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("datasources", type=str, nargs=-1, required=True)
def jinplate_cli(template_file, datasources, jinja_ext):
    """
    A command line renderer for jinja2 templates. If ansible is available, jinplate
    uses its template engine. If not, uses plain jinja2.

    TEMPLATE_FILE is the path to a jinja template file to render

    DATASOURCES is a list of URIs to data sources supported by jinplate which contain
    the template variables

    --jinja-ext allows specifying a comma-separated list of import paths containing
    jinja extensions. Example: --jinja-ext jinja2.ext.i18n
    """
    dataloader = DataLoader()
    data = {}
    for source in datasources:
        data = {**data, **dataloader.load(source)}

    extensions = jinja_ext.split(",") if jinja_ext is not None else []
    print(_render_template(template_file, extensions, **data))


# pylint: disable=no-value-for-parameter
if __name__ == '__main__':
    jinplate_cli()
