#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

TRINITY_DEP = "57bee06c9ad350ddfba1ae4b2081025aa454880d"

deps = {
    "trinity-eth2": [
        f"trinity @ git+https://github.com/ethereum/trinity.git@{TRINITY_DEP}",
        "libp2p>=0.5.0",
    ],
    "test": [
        "async-timeout>=3.0.1,<4",
        "hypothesis>=4.45.1,<5",
        "pexpect>=4.6, <5",
        "factory-boy==2.12.0",
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.10.0",
        "pytest-randomly>=3.12.0",
        "pytest-timeout>=2.1.0",
        "pytest-watch>=4.2.0,<4.3",
        "pytest-xdist>=3.0.0",
        # only for eth2
        "ruamel.yaml==0.16.10",
        "eth-tester==0.4.0b2",
    ],
    "test-trio": ["pytest-trio>=0.7.0"],
    "lint": [
        "flake8>=6.0.0",
        "flake8-bugbear>=23.0.0",
        "mypy>=1.0.0",
        "black>=23.0.0",
        "isort>=5.12.0",
    ],
    "dev": [
        "bumpversion>=0.5.3,<1",
        "wheel",
        "setuptools>=36.2.0",
        "tox>=4.0.0",
        "twine",
    ],
    "eth2": [
        "cytoolz>=0.9.0,<1.0.0",
        "eth-typing>=2.1.0,<3.0.0",
        "lru-dict>=1.1.6",
        "py-ecc==4.0.0",
        "rlp>=1.1.0,<2.0.0",
        "ssz==0.2.4",
        "asks>=2.3.6,<3",  # validator client
        "anyio>1.3,<1.4",
        "eth-keyfile",  # validator client
        "milagro-bls-binding==1.3.0",
    ],
}

deps["dev"] = (
    deps["dev"] + deps["trinity-eth2"] + deps["test"] + deps["lint"] + deps["eth2"]
)


install_requires = deps["trinity-eth2"] + deps["eth2"]


with open("./README.md") as readme:
    long_description = readme.read()


setup(
    name="trinity-eth2",
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version="0.1.0-alpha.0",
    description="The Trinity client for the Ethereum 2.0 network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ethereum Foundation",
    author_email="piper@pipermerriam.com",
    url="https://github.com/ethereum/trinity",
    include_package_data=True,
    py_modules=["trinity-eth2", "eth2"],
    python_requires=">=3.10,<4",
    install_requires=install_requires,
    extras_require=deps,
    license="MIT",
    zip_safe=False,
    keywords="ethereum 2.0 blockchain evm trinity",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    # trinity
    entry_points={
        "console_scripts": [
            "trinity-beacon=trinity:main_beacon_trio",
            "trinity-validator=trinity:main_validator",
        ]
    },
)
