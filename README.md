# Parser

## Installation

Create a venv called venv

```
python -m venv venv
```

Activate the venv - if running windows

```
venv\Scripts\activate
```

pip install requirements file

```
pip install -r requiremtnes.txt
```

pip install the module in editable mode

```
pip install -e .
```

Note that tabula library is being used. If you are Windows user make sure you have Java installed, instructions on how to set it up correctly found [here](https://tabula-py.readthedocs.io/en/latest/getting_started.html#get-tabula-py-working-windows-10).

## Usage

To run the extractor you can manually execute the main function run

```
python src/extractor/main.py
```

The main function run needs any YAML config file you want to use as the input. The config files contain all the user input, e.g. the pdf filename we want to use, the page number we want to extract the info from. Then it make an instance of the extractor class, and execute its various methods so that we extract, clean, transform, compute the stats and save the info as a csv.

## Future work

- Extend the config files to cover the extraction of pages 16 to 19
- Create a CLI to interact with the main function. Perhaps move away from having n number of config files and use something like Hydra, to override the config parameters on the fly
- Store the data in a SQL DB, e.g. PostgreSQL. Expand the schema to include timestamps for creation_time, last_update, etc
- Dockerfile: mind tabula, and its dependency with Java's JDK
