
[![PyPi](https://img.shields.io/pypi/v/ibmcloud-python-sdk.svg)](https://pypi.org/project/ibmcloud-python-sdk)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# IBM Cloud Python SDK

`ibmcloud-python-sdk` aims to talk to IBM Cloud. To do this, it requires a configuration file. `ibmcloud-python-sdk` favours `clouds.yaml` file, but can also use environment variables *(see [below](#environment-variables))*. An example:

```yaml
---
clouds:
  default: demo-acc
  demo-acc:
    profile: demo
    description: Credentials from my IBM Cloud demo account
    key: XxX1234567890XxX
    region: us-south
    version: 2021-06-15
    generation: 2
    cis_username: 000000_sponge.bob@sink.com
    cis_apikey: abc123def456ghi789klm0n
  prod-acc:
    profile: prod
    description: Credentials from my IBM Cloud production account
    key: zZz1234567890zZz
    region: us-south
    version: 2021-06-15
    generation: 2
    cis_username: 999999_sponge.bob@sink.com
    cis_apikey: @@abc123def456ghi789klm0n@@
```

The `clouds.yaml` file will be searched at first into `~/.ibmcloud` directory but this behavior could be overrided by an environment variable.

## Environment variables

| Variable           | Description | Example | Mandatory |
| ------------------ | ----------- | ------- | --------- |
| `IC_CONFIG_FILE`     | Absolute path to the `clouds.yaml` file | `~/vault/ibm.yaml` | [ ] |
| `IC_CONFIG_NAME`     | Name of the default cloud configuration | `demo` | [ ] |
| `IC_REGION`          | Region were to connect | `us-south` | [x] |
| `IC_VERSION`         | Requests the version of the API | `2021-06-15` | [x] |
| `IC_GENERATION`      | The infrastructure generation for the request | `2` | [x] |
| `IC_SDK_CONFIG_FILE` | Absolute path to the `sdk.yaml` file | `~/.config/ibmcloud/sdk.yaml` | [ ] |
| `IC_API_KEY`         | API key created via the IBM Cloud IAM system | `XxX1234567890XxX` | [x] |
| `SL_USERNAME`        | SoftLayer user | `goldyfruit` | [ ] |
| `SL_API_KEY`         | SoftLayer API key | `abc123def456ghi789klm0n` | [ ] |

## Installation

Install from PyPi via `pip`:

```shell
python -m venv ~/virtualenvs/ibmcloud-python-sdk
source ~/virtualenvs/ibmcloud-python-sdk/bin/activate
pip install ibmcloud-python-sdk
```

Or you can install from source:

```shell
cd ~/Git
git clone https://github.com/goldyfruit/ibmcloud-python-sdk.git
python -m venv ~/virtualenvs/ibmcloud-python-sdk
source ~/virtualenvs/ibmcloud-python-sdk/bin/activate
cd ~/Git/ibmcloud-python-sdk
pip install .
```

We recommend to use Python virtual environment to install the SDK.

## Caching

The SDK has caching capability *(`memcached` only for now)* to improve the HTTP requests speed. To enable this mechanisim please configure the SDK properly using `~/.ibmcloud/sdk.yaml` file.

```yaml
---
sdk:
  cache_ttl: 60
  memcached:
    - 127.0.0.1:11211
```

Muttiple cache servers could be configured as well.

```yaml
---
sdk:
  cache_ttl: 60
  memcached:
    - 127.0.0.1:11211
    - 127.0.0.1:11212
    - 127.0.0.1:11213
```

An easy way to deploy `memcached` server is to use container.

### Podman

```shell
podman run -dt -p 11211:11211 --name memcached -d memcached
```

### Docker

```shell
sudo docker run -dt -p 11211:11211 --name memcached -d memcached
```

## Examples

A list of examples on how to use this SDK can be found at [here](https://github.com/goldyfruit/ibmcloud-python-sdk/tree/main/examples).

### List VPCs

```python
from ibmcloud_python_sdk.vpc import vpc as ic


vpc = ic.Vpc()
vpc.get_vpc("ibmcloud-vpc-baby")
```

### Create a VPC instance

```python
from ibmcloud_python_sdk.vpc import instance as ic


instance = ic.Instance()
instance.create_instance(
  name="vm001", profile="cx2-4x8",
  resource_group="f328f2cdec6d4b4da2844c214dec9d39",
  vpc="r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765",
  image="r006-931515d2-fcc3-11e9-896d-3baa2797200f",
  pni_subnet="0737-f763775a-05d4-41fb-9da3-3cbd64530",
  zone="us-south-3"
)
```

## Copyright

See the bundled [LICENSE](https://github.com/goldyfruit/ibmcloud-python-sdk/blob/main/LICENSE) file for more information.
