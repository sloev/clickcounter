# ClickCounter

[![Latest Version](https://img.shields.io/pypi/v/clickcounter.svg)](https://pypi.python.org/pypi/clickcounter) [![PyPI - Downloads](https://img.shields.io/pypi/dm/clickcounter?label=pypi%20downloads)](https://pypistats.org/packages/clickcounter)

Create redirect url's with click monitoring from multiple providers.


### Features

* Growing list of click count providers (with a common lib interface)
* Commandline tool (CLI)
* Simple and easy to use

### Support the development ❤️

You can support the development by:

1. [Buying the maintainer a coffee](https://buymeacoffee.com/sloev)
2. [Buying some Lambdarest swag](https://www.redbubble.com/i/mug/Lambdarest-by-sloev/73793554.9Q0AD)

## Install

Install from pypi:

```bash
$ pip install clickcounter
```

## Usage (module)

> using the default provider (`shorturl.at`)

```python
import os
import time
import clickcounter

track_url = clickcounter.register_url("https://example.com")
print(track_url)
first_count = clickcounter.get_visits(track_url)
print(first_count)
clickcounter.make_visit(track_url)
time.sleep(2)
second_count = clickcounter.get_visits(track_url)
print(second_count)

# https://shorturl.at/iANR5
# 0
# 1
```

**more examples here:**

* [shorturl.at example](https://github.com/sloev/clickcounter/examples/shorturl_at.py)
* [linkclickcounter.com example](https://github.com/sloev/clickcounter/examples/linkclickcounter_com.py)


## Usage (CLI)

```bash

usage: _cli.py [-h] [--provider PROVIDER] [--username USERNAME] [--password PASSWORD] [--url URL] [--trackurl TRACKURL]
               command

positional arguments:
  command              valid commands: register, get, getall

optional arguments:
  -h, --help           show this help message and exit
  --provider PROVIDER  defaults to shorturl.at
  --username USERNAME  some providers require login
  --password PASSWORD  some providers require login
  --url URL            used during register
  --trackurl TRACKURL  used during get
```

**example**: 

```bash

$ clickcounter register --url https://example.com
https://shorturl.at/wABHQ

# visit the link in browser...
# and then get click count via:

$ clickcounter get --trackurl https://shorturl.at/wABHQ
1
```