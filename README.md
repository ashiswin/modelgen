# ModelGen

This project consists of a set of scripts that allow you to easily generate model code files to interact with a set of MySQL tables in a database. Currently the generated model files are in PHP. It has been written in a modular fashion to allow for the addition of more output languages.

## Getting Started

Simply clone this repository to get started. Once set up, just run

```
python generator.py
```
to launch the generator tool. The tool will generate a directory structure as follows:
```
./<dbname>
./<dbname>/connectors
./<dbname>/util
```

The connectors folder contains all the model code files while the util folder contains the database connection configuration.

### Prerequisites

This project depends on the following packages:

```
pip install mysql-connector
pip install pattern
```

It was written for Python 2.7, but can work with slight modifications in Python 3+.

## License

This project is licensed under the MIT License.
