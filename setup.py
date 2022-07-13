import setuptools

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setuptools.setup(
    name="leeger",
    version="0.1.0",
    author="Joey Greco",
    author_email="joeyagreco@gmail.com",
    description="Leeger is a python library for instantly loading Fantasy Football stats for any league.",
    long_description=readme,
    license=license,
    packages=setuptools.find_packages(exclude=("test", "docs")),
    install_requires=["numpy",
                      "setuptools",
                      "openpyxl",
                      "espn-api",
                      "yahoofantasy"]
)
