import setuptools

pkg_vars = dict()
with open("leeger/_version.py") as f:
    exec(f.read(), pkg_vars)

with open("README.md") as f:
    readme = f.read()

setuptools.setup(
    name="leeger",
    version=pkg_vars["__version__"],
    author="Joey Greco",
    author_email="joeyagreco@gmail.com",
    description="Instant stats for your fantasy football league.",
    long_description_content_type="text/markdown",
    long_description=readme,
    license="MIT",
    packages=setuptools.find_packages(exclude=("test", "docs")),
    install_requires=["numpy",
                      "setuptools",
                      "openpyxl",
                      "espn-api",
                      "yahoofantasy",
                      "sleeper"]
)
