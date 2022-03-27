from pathlib import Path
from typing import Union
from zipfile import ZipFile

import click
import jinja2

from ._project import DEFAULT_DATABASE, PROJECT_DIR, SQL_DIR, TARGET_DIR, DATA_DIR, get_connection, get_config


@click.group()
@click.help_option("-h", "--help")
def cli():
    pass


@cli.command()
def download_chinook():
    import requests

    response = requests.get("http://robbmann.io/chinook.zip")

    if not response.ok:
        response.raise_for_status()

    chinook_zip = DATA_DIR / "chinook.zip"
    chinook_zip.parent.mkdir(parents=True, exist_ok=True)

    with open(chinook_zip, "wb") as destination:
        for chunk in response.iter_content(chunk_size=8192):
            destination.write(chunk)

    with ZipFile(chinook_zip, "r") as zip:
        zip.extractall(DATA_DIR)

    chinook_zip.unlink()


@cli.command()
@click.argument("path")
def ctas(path: Union[str, Path]):
    """
    Create a new table in the analysis database using the SQL file found at
    `path.`  The name of the table will match the filename: sql/tablename.sql
    --> `tablename` in `analysis.db`
    """
    path = Path(path)
    config = get_config()

    jinja_loader = jinja2.FileSystemLoader(path.parent)
    jinja_environment = jinja2.Environment(loader=jinja_loader)
    template = jinja_environment.get_template(str(path.name))

    sql = f"""
        DROP TABLE IF EXISTS {path.stem};
        CREATE TABLE {path.stem} AS {template.render(**config)}
    """

    with get_connection() as con:
        con.executescript(sql)


def customer_sales():
    import pandas as pd

    with get_connection() as con:
        return pd.read_sql("SELECT * FROM customer_sales;", con)


@cli.command()
def customer_sales_csv():
    df = customer_sales()
    df.to_csv(TARGET_DIR / "customer_sales.csv", index=False)


@cli.command()
def customer_sales_chart():
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    s = customer_sales().set_index("state")
    assert s is not None
    s.plot(kind="bar", ax=ax)
    fig.savefig(TARGET_DIR / "customer_sales.png")
