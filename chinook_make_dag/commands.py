import click

from ._project import DEFAULT_DATABASE, PROJECT_DIR, SQL_DIR, TARGET_DIR


@click.group()
@click.help_option("-h", "--help")
def cli():
    pass


@cli.command()
def info():
    print(f"Project description: {get_config()['description']}")
    print(f"Project directory: {PROJECT_DIR.absolute()}")
    print(f"Default database: {DEFAULT_DATABASE}")


@cli.command()
def download_chinook():
    import requests

    response = requests.get("http://robbmann.io/chinook.zip")

    if not response.ok:
        return


@cli.command()
def customer_count_csv():
    import pandas as pd

    df = pd.DataFrame(dict(a=range(3), b=list("abc")))
    df.to_csv(TARGET_DIR / "member_count.csv", index=False)


@cli.command()
def customer_count_chart():
    import pandas as pd
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    df = pd.DataFrame(dict(a=range(3), b=list("abc")))
    df.plot(kind="bar", ax=ax)
    fig.savefig(TARGET_DIR / "member_count.png")
