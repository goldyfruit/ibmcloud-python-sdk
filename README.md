IBM Cloud Python SDK
====================

This library provides Python client to interact with IBM Cloud REST APIs.

IBM Cloud Python SDK leverages existing Python SDKs such as:
  - [SoftLayer](https://github.com/softlayer/softlayer-python)
  - [IBM Cloud Object Storage](https://github.com/IBM/ibm-cos-sdk-python)

Documentation
-------------
Documentation for the Python client is available at https://XXXXXXX.XXX.


Installation
------------
Install via `pip`:

    $ pip install ibmcloud-python-sdk

Or you can install from source. Download source and run:

    $ python setup.py install

Another *(safer)* method of installation is to use the published snap. Snaps are available for any Linux OS running `snapd`, the service that runs and manage snaps. Snaps are "auto-updating" packages and will not disrupt the current versions of libraries and software packages on your Linux-based system. To learn more, please visit: https://snapcraft.io/ 

To install the `ibmcloud-python-sdk` snap:

    $ sudo snap install ibmcloud-python-sdk
	
The most up-to-date version of this library can be found on the IBM-Cloud
GitHub public repositories at https://github.com/IBM-Cloud. For questions regarding the use of this library please post to Stack Overflow at https://stackoverflow.com/ and tag your posts with `ibmcloud` so our team can easily find your post. To report a bug with this library please create an Issue on Github.

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
Bugs and feature requests about this library should have a `GitHub issue <https://github.com/IBM-Cloud/ibmcloud-python-sdk/issues>`_ opened about them. 


Examples
--------
A curated list of examples on how to use this library can be found at XXXXXXXX

Requirements
-------------------
* Python >= 3.5
* A valid IBM Cloud account with a valid API key configured.

Python 2.7 Support
------------------
IBM Python Cloud SDK doesn't support python2.7, which is `End Of Life as of 2020 <https://www.python.org/dev/peps/pep-0373/>`_ .

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
