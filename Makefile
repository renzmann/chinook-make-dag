# "functions"
to_command = python -m $(PROJECT) $(shell echo $(subst _,-,$(1)) | tr '[:upper:]' '[:lower:]')
from_import = $(shell python -c "import $(PROJECT); print($(PROJECT).$(1))")

# Directories to search
PROJECT := $(notdir $(subst -,_,$(CURDIR)))
TARGETDIR := $(call from_import,TARGET_DIR)
SQLDIR := $(call from_import,SQL_DIR)
DATADIR := $(call from_import,DATA_DIR)
AUTODIR := $(TARGETDIR)/auto
VPATH := $(SQLDIR):$(TARGETDIR):$(AUTODIR):$(DATADIR)

# Automatic targets from all SQL files
OBJS := $(wildcard $(SQLDIR)/*.sql)
TARGETS := $(patsubst $(SQLDIR)/%.sql,%.ctas,$(OBJS))

# Parallel job execution - comment out this line to have all tasks run sequentially
MAKEFLAGS := --jobs=$(shell nproc)

# By default, construct all the analytics tables
tables: $(TARGETS)

# ============================= Main DAG ====================================
# The main table and file dependency graph goes here, of the form:
#   target(s): one or more dependencies
#
# Athena table, requires sql/<name>.sql to exist
#   ^<name>
#
# Flat files, requires the python function `<name>_csv` or `<name>_excel` in <project>/commands.py
#   <name>.csv/.xlsx
#
# Visualizations, requires the python function `<name>_chart` in <project>/commands.py
#   <name>.png/.svg/.html
analysis_customers.ctas:
customer_count.ctas: analysis_customers.ctas
customer_sales.ctas: analysis_customers.ctas
customer_sales.png customer_sales.csv: customer_sales.ctas

# ========================= Automatic Rules =================================
# Empty targets ending with ".ctas" indicate a completed CTAS execution
%.ctas: %.sql | $(TARGETDIR) database
	python -m $(PROJECT) ctas $<
	@touch $(AUTODIR)/$@

pyfunc_%: $(PROJECT) | $(TARGETDIR)
	$(call to_command,$(patsubst pyfunc_%,%,$@))
	touch $(AUTODIR)/$@

%.jpg %.png %.html %.svg:
	$(call to_command,$*)-chart

%.xlsx:
	$(call to_command,$*)-excel

%.csv:
	$(call to_command,$*)-csv

# =========================== Misc. Content =================================
.PHONY: data install

$(TARGETDIR):
	mkdir -p $(TARGETDIR)
	mkdir -p $(AUTODIR)

$(DATADIR):
	mkdir -p $(DATADIR)
	python -m $(PROJECT) download-chinook

data: $(DATADIR)

$(TARGETS): config.yml $(PROJECT)

clean:
	@[ ! -d $(TARGETDIR) ] || rm -r $(TARGETDIR)
	@[ ! -d $(DATADIR) ] || rm -r $(DATADIR)

install: data
	@pip install --upgrade pip wheel
	@curl -sSL https://install.python-poetry.org | python3 -
	@~/.local/bin/poetry install --no-dev
