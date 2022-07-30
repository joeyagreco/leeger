import setuptools

from _version import __version__ as version

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license_ = f.read()

setuptools.setup(
    name="leeger",
    version=version,
    author="Joey Greco",
    author_email="joeyagreco@gmail.com",
    description="Instant stats for your fantasy football league.",
    long_description_content_type="text/markdown",
    long_description=readme,
    license=license_,
    packages=setuptools.find_packages(exclude=("test", "docs")),
    install_requires=["numpy",
                      "setuptools",
                      "openpyxl",
                      "espn-api",
                      "yahoofantasy",
                      "sleeper"]
)
