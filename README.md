# Building a Simple DAG project with Make, SQL, and Python 

This is the companion code to demonstrate a working example built
off my article [of the same name.][dag-article]  It is a simple template/example
of a working ELT project where we take some data, the Chinook dataset, and
produce some analysis tables from it, along with accompanying data/visual
exports.

[dag-article]: <https://robbmann.io/posts/make_dag> "Explanatory article on my blog"

# Installation

Use `make install` from the top level of this repository.  This will install
`poetry` to `~/local/bin/poetry`, and use it to install this project along with
all its python dependencies.

```sh
git clone https://github.com/renzmann/chinook-make-dag && cd chinook-make-dag
python3 -m venv .venv
source .venv/bin/activate
make install
```

If you do not want to use poetry, you can use a recent version of `pip` to
install in editable mode as well:

```sh
pip install --upgrade pip wheel
pip install -e .
make data
```

# Usage

`make tables` will produce new tables in `data/analysis.db` for each SQL file in
the `sql/` directory.  A couple examples are provided for hard artifacts:

`make customer_sales.png` will produce a bar chart in the `target/` directory
with total sales of US customers within each state.  `make customer_sales.csv`
produces a CSV with the data this chart uses.

If at any point you want to refresh your `target/` or `data/` directories, you
can use `make clean` and `make data`.
