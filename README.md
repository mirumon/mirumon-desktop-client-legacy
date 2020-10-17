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

View all available teams:

```bash
mirumon --help
```

Install the client as a service and run:

* Note: Do not forget to run  the terminal as administrator
```bash
mirumon install wss://your-mirumon-server.com/service servertoken
# example 
mirumon run wss://your-mirumon-server.com/service 718fedaeb5006380e37998aa867eb21e
```

Basic commands for managing a service: 
```bash
mirumon start
mirumon restart
mirumon stop
mirumon remove
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
mirumon --help
```
Use `nuitka` to convert python code to `.exe`:
* Note: Install mingw64 

```bash
python -m nuitka --standalone --windows-dependency-tool=pefile --experimental=use_pefile_recurse --experimental=use_pefile_fullrecurse --follow-imports  --mingw64 --show-progress .\mirumon\cli\mirumon.py
```
