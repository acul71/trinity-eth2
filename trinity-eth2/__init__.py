import pkg_resources
import sys

# TODO: update this to use the `trinity` version once extracted from py-evm
__version__: str
try:
    __version__ = pkg_resources.get_distribution("trinity").version
except pkg_resources.DistributionNotFound:
    try:
        __version__ = f"eth-{pkg_resources.get_distribution('py-evm').version}"
    except pkg_resources.DistributionNotFound:
        __version__ = "unknown"


# Setup the `DEBUG2` logging level
try:
    from eth_utils import setup_DEBUG2_logging  # noqa: E402
    setup_DEBUG2_logging()
except Exception:
    pass


def is_uvloop_supported() -> bool:
    return sys.platform in {'darwin', 'linux'} or sys.platform.startswith('freebsd')


if is_uvloop_supported():
    # Set `uvloop` as the default event loop
    import asyncio
    try:
        from eth._warnings import catch_and_ignore_import_warning
        with catch_and_ignore_import_warning():
            import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except Exception:
        pass


# Lazy imports to avoid pulling in the entire dependency tree on import.
# The old eager imports cause cascading import failures on Python 3.12+
# due to incompatible transitive deps in the old trinity package.
def __getattr__(name):
    if name == 'main_beacon_trio':
        try:
            from .main_beacon_trio import main_beacon as main_beacon_trio
            return main_beacon_trio
        except ImportError:
            raise AttributeError(f"module 'trinity' has no attribute '{name}'")
    if name == 'main_validator':
        try:
            from .main_validator import main_validator
            return main_validator
        except ImportError:
            raise AttributeError(f"module 'trinity' has no attribute '{name}'")
    raise AttributeError(f"module 'trinity' has no attribute '{name}'")
