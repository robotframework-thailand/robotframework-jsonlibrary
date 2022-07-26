import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))
version = {}
with open(os.path.join(HERE, "JSONLibrary", "__version__.py"), encoding="utf8") as f:
    exec(f.read(), version)

requirements = ["robotframework>=3.0", "jsonpath-ng>=1.4.3", "jsonschema>=2.5.1"]

setup(
    name="robotframework-jsonlibrary",
    version=version["__version__"],
    description="robotframework-jsonlibrary is a Robot Framework "
    "test library for manipulating JSON Object. "
    "You can manipulate your JSON object using JSONPath",
    author="Traitanit Huangsri",
    author_email="traitanit.hua@gmail.com",
    url="https://github.com/nottyo/robotframework-jsonlibrary.git",
    packages=["JSONLibrary"],
    package_dir={"robotframework-jsonlibrary": "JSONLibrary"},
    install_requires=requirements,
    keywords="testing robotframework json jsonschema jsonpath",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: Public Domain",
        "Programming Language :: Python :: 3",
        "Framework :: Robot Framework :: Library",
    ],
)
