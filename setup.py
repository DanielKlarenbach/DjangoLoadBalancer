import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
VERSION = '0.0.10'
PACKAGE_NAME = 'djangoloadbalancer'
AUTHOR = 'Daniel Klarenbach'
URL = 'https://github.com/DanielKlarenbach/DjangoLoadBalancer'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Package enabling to load balance requests to databases in django projects'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
INSTALL_REQUIRES = [

]

setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    url=URL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    install_requires=INSTALL_REQUIRES,
    packages=setuptools.find_packages(),
)


