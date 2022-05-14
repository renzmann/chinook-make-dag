# Building a Simple DAG project with Make, SQL, and Python

This is the companion code to demonstrate a working example built
off my article [of the same name.][dag-article]  It is a simple template/example
of a working ELT project where we take some data, the Chinook dataset, and
produce some analysis tables from it, along with accompanying data/visual
exports.

[dag-article]: <https://robbmann.io/posts/make_dag> "Explanatory article on my blog"

# Setup and installation

Since this is a _project template_, it assumes you'll be copying down this
folder, editing SQL, and running commands via `make` yourself.  This comes with two prerequisites:

1. Python >= 3.8
2. `make` - usually distributed as GNU Make

Linux/macOS usually have both of these readily available.  On Windows, you will
need either the [Windows Subsystem for Linux
(WSL)](https://docs.microsoft.com/en-us/windows/wsl/install) (recommended), or
[MinGW](https://www.mingw-w64.org/) with `git` and `make` installed.

To get the project locally, simply clone it:

```sh
git clone https://github.com/renzmann/chinook-make-dag && cd chinook-make-dag
```

## (Recommended) installation - via `poetry`

If you are on linux, macOS, or WSL, use `make install` from the top level of this repository.
This will install `poetry` to `~/.local/bin/poetry`, and use it to install this project along with
all its python dependencies.

```sh
make install
```

If you are not on linux/macOS/WSL, I still recommend [installing poetry
yourself](https://python-poetry.org/docs/master/#installing-with-the-official-installer),
and using it to install the project, since it takes care of all the virtual
environment overhead for you.

```sh
poetry install
```

## Manual installation

If you do not want to use poetry, you can use a
recent version of `pip` to install in editable mode:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip wheel
pip install -e .
```

# Usage

All of the commands below are prefixed with `poetry run` - if you did not
install via poetry, or have already run the `poetry shell` command to activate
your poetry environment, do not include the `poetry run` part:

```sh
# Installed via poetry and NOT in poetry shell:
poetry run make tables

# In poetry shell or manual virtual environment installation
make tables
```

`make tables` will produce new tables in `data/analysis.db` for each SQL file in
the `sql/` directory.  A couple examples are provided for hard artifacts:

1. `poetry run make customer_sales.png` will produce a bar chart in the `target/` directory
   with total sales of US customers within each state.
3. `poetry run make customer_sales.csv` produces a CSV with the data this chart uses.

If at any point you want to refresh your `target/` or `data/` directories, you
can use `poetry run make clean`.
