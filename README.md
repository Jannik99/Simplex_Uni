# Setup

## 1. Setup Virtual Environment

a) run: `pip install virtualenv`<br>
b) if there is no folder "./venv" run: `mkdir venv`<br>
c) run: `virtualenv venv`<br>

## 2. Activate Virtual Environment

### On Windows

run: `.\venv\Scripts\activate.bat`

### On MacOS/Linux

run: `source ./venv/bin/activate`

### Install Numpy
<strong>Note: </strong>This step is only required if you installed a fresh virtualenv:<br>´pip install numpy´

# Add new Benchmarks

a) go to "./simplex-solver/benchmarks"<br>
b) make a new .txt file<br>
c) insert conditions for a new Benchmark following the pattern of the existing ones

<div style="border: 1px dashed grey; padding: 4px"><strong>Note: </strong>If its a minimization, write "min:" in front of the Objective function, if its a maximization, write "max:" in front of the Objective function</div>

# Run Software

## Only run Parser

a) go to "./simplex-solver":

```
cd ./simplex-solver
```

b) run the parser

```
python -c 'import parser; parser.getParsedBenchmarks()'
```

## Run Simplex with Parser

a) go to "./simplex-solver"<br>
b) run the solver

```
python main.py
```

The programm will run all Benchmarks inside the benchmarks-folder. Since there is a Problem with KI_20 and KI_30, it will run forever if they are inside this folder.
