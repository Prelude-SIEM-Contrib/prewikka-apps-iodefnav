from setuptools import setup, find_packages

setup(
    name="prewikka-apps-iodefnav",
    version="3.0.0",
    author="Prelude Team",
    author_email="support.prelude@c-s.fr",
    url="https://prelude-siem.org",
    packages=find_packages(),

    install_requires=[
        'prewikka >= 3.0.0',
        'pyyaml'
    ],
    entry_points={
        "prewikka.views": [
            "IODEFnav = iodefnav:IODEFNav",
        ],
    },
    package_data={
        "iodefnav": [
            "htdocs/yaml/*.yml", "htdocs/graph/*", "templates/*.py"
        ],
    },
)
