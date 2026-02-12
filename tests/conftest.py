import asyncio
import contextlib
import logging
import os
from pathlib import Path
import tempfile
import uuid

import pytest

# Guard trinity/eth imports - these require the old trinity package which
# is not fully compatible with Python 3.12+. Tests that need these fixtures
# will be skipped if imports fail.
_TRINITY_AVAILABLE = False
try:
    from eth.chains.base import Chain
    from eth.db.atomic import AtomicDB
    from lahja import AsyncioEndpoint, ConnectionConfig
    from trinity._utils.filesystem import is_under_path
    from trinity._utils.xdg import get_xdg_trinity_root
    from trinity.chains.coro import AsyncChainMixin
    from trinity.config import TrinityConfig
    from trinity.constants import NETWORKING_EVENTBUS_ENDPOINT
    from trinity.initialization import initialize_data_dir
    _TRINITY_AVAILABLE = True
except (ImportError, AttributeError, TypeError) as e:
    import warnings
    warnings.warn(f"trinity package not fully available (Python 3.12+ compat): {e}")


def pytest_addoption(parser):
    parser.addoption("--enode", type=str, required=False)
    parser.addoption("--integration", action="store_true", default=False)
    parser.addoption("--silence_async_service", action="store_true", default=False)
    parser.addoption("--fork", type=str, required=False)


if _TRINITY_AVAILABLE:
    class TestAsyncChain(Chain, AsyncChainMixin):
        pass


@pytest.fixture(scope="session", autouse=True)
def silence_loggers(request):
    if request.config.getoption("--silence_async_service"):
        logging.getLogger("async_service").setLevel(logging.INFO)


@pytest.fixture(autouse=True)
def xdg_trinity_root(monkeypatch, tmpdir):
    """
    Ensure proper test isolation as well as protecting the real directories.
    """
    if not _TRINITY_AVAILABLE:
        yield Path(tmpdir) / "trinity"
        return
    with tempfile.TemporaryDirectory() as tmp_dir:
        xdg_root_dir = Path(tmp_dir) / "trinity"
        monkeypatch.setenv("XDG_TRINITY_ROOT", str(xdg_root_dir))
        assert not is_under_path(os.path.expandvars("$HOME"), get_xdg_trinity_root())
        yield xdg_root_dir


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@contextlib.asynccontextmanager
async def make_networking_event_bus():
    if not _TRINITY_AVAILABLE:
        raise RuntimeError("trinity package not available")
    # Tests run concurrently, therefore we need unique IPC paths
    ipc_path = Path(f"networking-{uuid.uuid4()}.ipc")
    networking_connection_config = ConnectionConfig(
        name=NETWORKING_EVENTBUS_ENDPOINT, path=ipc_path
    )
    async with AsyncioEndpoint.serve(networking_connection_config) as endpoint:
        yield endpoint


@pytest.fixture
async def event_bus():
    async with make_networking_event_bus() as endpoint:
        yield endpoint


# Tests with multiple peers require us to give each of them there independent 'networking' endpoint
@pytest.fixture
async def other_event_bus():
    async with make_networking_event_bus() as endpoint:
        yield endpoint


@pytest.fixture(scope="session")
def jsonrpc_ipc_pipe_path():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir) / "{0}.ipc".format(uuid.uuid4())


@pytest.fixture
def trinity_config():
    if not _TRINITY_AVAILABLE:
        pytest.skip("trinity package not available on Python 3.12+")
    _trinity_config = TrinityConfig(network_id=1)
    initialize_data_dir(_trinity_config)
    return _trinity_config


@pytest.fixture
def base_db():
    if not _TRINITY_AVAILABLE:
        pytest.skip("trinity package not available on Python 3.12+")
    return AtomicDB()
