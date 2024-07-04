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
    Main CLI script for jinplate
    :param template_file: Path to a Jinja2 template file
    :param datasource: URI of the data source to use as template parameters
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
