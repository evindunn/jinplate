#!/usr/bin/env python3

import pathlib

import click
import jinja2

from jinplate.plugins.loader import DataLoader


@click.command("jinplate")
@click.argument("template_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("datasource", type=str)
def jinplate_cli(template_file, datasource):
    """
    A command line renderer for jinja templates

    TEMPLATE_FILE is the path to a jinja template file to render

    DATASOURCE is the URI of a datasource supported by jinplate that contains the
    template variables
    """
    template_path = pathlib.Path(template_file)
    jenv = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path.parent))
    template = jenv.get_template(template_file)

    dataloader = DataLoader()
    data = dataloader.load(datasource)

    print(template.render(data))


# pylint: disable=no-value-for-parameter
if __name__ == '__main__':
    jinplate_cli()
