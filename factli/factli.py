from factli.get_posts import posts
from factli.get_list import lists
from factli.get_leaderboard import leaderboard
import click


@click.group()
def cli():
    pass

cli.add_command(lists)
cli.add_command(posts)
cli.add_command(leaderboard)

if __name__ == "__main__":
    cli()
