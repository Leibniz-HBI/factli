from factli.get_posts import posts
from factli.get_list import lists
import click


@click.group()
def cli():
    pass

cli.add_command(lists)
cli.add_command(posts)

if __name__ == "__main__":
    cli()
