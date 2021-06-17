IBM Cloud Python SDK
====================

This library provides Python SDK to interact with IBM Cloud REST APIs.

IBM Cloud Python SDK leverages existing Python SDKs such as:
  - [SoftLayer](https://github.com/softlayer/softlayer-python)
  - [IBM Cloud Object Storage](https://github.com/IBM/ibm-cos-sdk-python)

Documentation
-------------
Documentation for the IBM Cloud Python SDK is available [here](https://goldyfruit.github.io/ibmcloud-python-sdk).

Installation
------------
Install via `pip`:

    $ pip install ibmcloud-python-sdk

Or you can install from source. Download source and run:

    $ python setup.py install
Caching
-------
IBM Cloud Python SDK has a capability to connect to a caching server *(`memcached` only for now)* to increase the HTTP requests speed. To enable the caching system please configure the SDK properly using `~/.ibmcloud/sdk.yaml` file.

    ---
    sdk:
      cache_ttl: 60
      memcached:
        - 127.0.0.1:11211
        - 127.0.0.1:11212
        - 127.0.0.1:11213

Once configured, a `memcached` server is required.

### Podman

    $ podman run -dt -p 11211:11211 --name memcache -d memcached

### Docker

    $ sudo docker run -dt -p 11211:11211 --name memcache -d memcached

Getting Help
------------
Bugs and feature requests about this SDK should have a [issue](https://github.com/goldyfruit/ibmcloud-python-sdk/issues) opened about them. 

Examples
--------
A curated list of examples on how to use this library can be found at https://github.com/goldyfruit/ibmcloud-python-sdk/tree/main/examples

Requirements
-------------------
* Python >= 3.5
* A valid IBM Cloud account with a valid API key configured.

Python Packages
---------------
* `PyYAML`>=3.12
* `rednose`==1.3.0
* `nose`==1.3.7
* `mock`==4.0.2
* `SoftLayer`==5.8.7
* `PyJWT`==1.7.1
* `ibm-cos-sdk`==2.6.2

Copyright
---------
See the bundled LICENSE file for more information.