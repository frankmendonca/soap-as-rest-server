# Soap Proxy

This is a "proxy" to SOAP protocol using REST.

## Installing

```bash
$ pip3 install soap-proxy
```

## Using as module

```bash
$ python3 -m soap-proxy
```

# Importing and using

```python
#!/usr/bin/env python3

import os
from os import path
from soap_proxy import start

base_dir = 'src'
os.environ['CONFIG_FILE'] = path.join(base_dir, 'config.yml')
os.environ['TEMPLATE_FILE'] = path.join(base_dir, 'template.xml')

os.environ['SERVER_PORT'] = '8080'
os.environ['SERVER_ENDPOINT'] = '/soap-proxy/'

start()
```
