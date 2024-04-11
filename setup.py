from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "Connection planning for MISO modules"
LONG_DESCRIPTION = 'The connection planning algorithms for modular self-reconfiguration robots composed of Multiple In-degree Single Out-degree (MISO) modules'

setup(
    name="MISO_planning",
    version=VERSION,
    author="Haobo Luo",
    author_email="<hoporluo@outlook.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["anytree",
                      "numpy>=1.23.2",
                      # "pickle",
                      # "graphviz",
                      # "collections",
                      # "copy",
                      # "itertools"
                      ],  # add any additional packages that
)
