import os
import click

from badwing.main import main

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:
      main()

@cli.command()
@click.pass_context
@click.argument('levelname', required=False)
def dev(ctx, levelname=None):
    main(debug=True, levelname=levelname)

@cli.command()
@click.pass_context
def run(ctx):
    main()
