# Mirumon Desktop Client

## Description

Simple monitoring client for desktop. It can collect data about the operating system, hardware, software, etc.

#### Windows  

It use [wmi](http://timgolden.me.uk/python/wmi/index.html) to collect data on windows.

For easier installation of the service, python code is translated into `.exe` using [nuitka](https://github.com/Nuitka/Nuitka).
After that, the executable is installed as a **windows service** using [nssm](https://nssm.cc/).

#### Linux

*Coming soon...*

## Usage

View all available commands:

```bash
mirumon --help
mirumon <command> --help
```

Install the client as a service and run:

* Note: Do not forget to run  the terminal as administrator
```bash
mirumon install wss://your-mirumon-server.com/service servertoken
# example 
mirumon run wss://your-mirumon-server.com/service eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ehth...Q.24fEekbD2JJq_ULs9fGyRVPD_v67c-QDoFnJ89pf-XI
```

Basic commands for managing a service: 
```bash
run      # run service in shell without installing as service

install  # install client as service (daemon) on pc
remove   # remove service from pc. stop service before it

start    # start installed service
stop     # stop installed service
restart  # restart installed service
```

## Develop
Mirumon client uses [poetry](https://github.com/python-poetry/poetry) as a package manager. 
You can easily install all the dependencies with the following commands:

```bash
pip install poetry
poetry install
```

After installation, you can use client cli:

```bash
poetry run mirumon --help
```
Use `nuitka` to convert python code to `.exe`:
* Note: Install mingw64. See `nuitka` docs for more info. 

```bash
python -m nuitka --standalone --windows-dependency-tool=pefile --experimental=use_pefile_recurse --experimental=use_pefile_fullrecurse --output-dir=_build --follow-imports --mingw64 --show-progress .\mirumon\cli\mirumon.py
```
