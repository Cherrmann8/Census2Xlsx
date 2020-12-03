# Cen2Xlsx

Author: Charles W. Herrmann

Date: 12/2/2020

# Quickstart

Clone the repository:

```bash
$ git clone https://github.com/Cherrmann8/Cen2Xlsx.git
```

Install the dependencies (requires [pip3](https://pypi.org/project/pip/)):

```bash
$ make install
```

# Overview

Cen2Xlsx is a cross-platform data collection tool for generating community needs assessment reports using the United States Census Bureau database. Developed with Python 3.7 and Kivy 1.11. The project has a Trello board for tracking features and development tasks. This board can be viewed at: https://trello.com/b/UD66VbiG/cen2xlsx.

# Usage

The application will be built into executables for Windows and macOS systems using Pyinstaller. These will eventually be available in the dist directory.

## Source Code Flags

Run the model without the GUI:

```bash
$ python3 src/model.py
```

### `-h` or `--help`

Print usage information.

### `-v` or `--verbose`

Logs additional output to a file in `/logs`.

### `-i` or `--input`

The input directory containing the cached json files. Run using:

```bash
$ python3 src/model.py -i INPUTDIR
# or
$ python3 src/model.py --input INPUTDIR
```

### `-o` or `--output`

The output directory containing the generated reports. Run using:

```bash
$ python3 src/model.py -o OUTPUTDIR
# or
$ python3 src/model.py --output OUTPUTDIR
```

# Design Discussion

## Design Benefits

This application was designed around a fast and simple user experience. Data is cached and included in the built application to significantly speed up the applications responsiveness and is consistent across survey types and years. The GUI was prototyped in Tkinter first to get a feel for how to enrich the user journey once the basic features were implemented.

## Limitations

- The library used for accessing the Census Database will rarely timeout and require a repeat of the data request.

## Code Style

Formatted using [Black](https://github.com/ambv/black). Linted using [PyLint](https://www.pylint.org/).
