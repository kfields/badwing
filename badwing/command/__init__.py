import os
import click

from badwing.main import main

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

@cli.command()
@click.pass_context
@click.argument('levelname', required=False)
def dev(ctx, levelname=None):
    main(debug=True, levelname=levelname)

@cli.command()
@click.pass_context
def run(ctx):
    main()
