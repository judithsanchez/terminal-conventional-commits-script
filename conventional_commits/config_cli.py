import click
from .config.config_manager import ConfigManager
from .colors import Colors

@click.group()
def cli():
    """Manage conventional commit types configuration"""
    pass

@cli.command()
@click.argument('type_name')
@click.argument('emoji')
def add(type_name, emoji):
    """Add a new commit type"""
    config = ConfigManager()
    config.add_commit_type(type_name, emoji)
    click.echo(f"{Colors.SUCCESS}Added commit type: {type_name} {emoji}")

@cli.command()
@click.argument('type_name')
def remove(type_name):
    """Remove a commit type"""
    config = ConfigManager()
    config.remove_commit_type(type_name)
    click.echo(f"{Colors.SUCCESS}Removed commit type: {type_name}")

@cli.command()
@click.argument('type_name')
@click.argument('new_emoji')
def modify(type_name, new_emoji):
    """Modify a commit type emoji"""
    config = ConfigManager()
    config.modify_commit_type(type_name, new_emoji)
    click.echo(f"{Colors.SUCCESS}Modified commit type: {type_name} {new_emoji}")

@cli.command()
def list():
    """List all commit types"""
    config = ConfigManager()
    types = config.load_commit_types()
    for type_name, emoji in types.items():
        click.echo(f"{Colors.OUTPUT}{type_name}: {emoji}")

@cli.command()
def reset():
    """Reset commit types to defaults"""
    config = ConfigManager()
    config.reset_to_defaults()
    click.echo(f"{Colors.SUCCESS}Reset commit types to defaults")

if __name__ == '__main__':
    cli()
