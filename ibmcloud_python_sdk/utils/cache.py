from pymemcache.client import base
from pymemcache.client import hash
from ibmcloud_python_sdk.config import sdk


config = sdk()


def client():
    """Create and configure memcached client

    :return: memcached client
    :rtype: map
    """
    if config:
        # Check if memcached is configured in sdk.yaml file
        if config.get("memcached") and len(config.get("memcached")) > 0:
            cache = []
            for node in config.get("memcached"):
                cache.append([node.split(":")[0], node.split(":")[1]])

            if len(config.get("memcached")) > 1:
                nodes = map(lambda x: (x[0], int(x[1])), cache)

                return hash.HashClient(nodes)

            node = config.get("memcached")[0]
            node = (node.split(":")[0], int(node.split(":")[1]))

            return base.Client(node)

    return False


def get_item(item_key):
    """Retrieve object from memcache

    :param item_key: Item key to retrieve
    :type item_key: str
    :return: Item value
    :rtype: str
    """
    return client().get(item_key)


def set_item(item_key, item_value):
    """Store object into memcached

    :param item_key: Item key to store
    :type item_key: str
    :param item_value: Item value to store
    :type item_value: str
    """
    if config:
        # Set expire to 60 secondes if not defined in sdk.yaml
        client().set(item_key, item_value, expire=config.get("cache_ttl", 60))
