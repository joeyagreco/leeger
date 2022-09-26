import setuptools

pkg_vars = dict()
with open("leeger/_version.py") as f:
    exec(f.read(), pkg_vars)

package_version = pkg_vars["__version__"]
minimum_python_version_required = pkg_vars["__version_minimum_python__"]

with open("README.md") as f:
    readme = f.read()

setuptools.setup(
    name="leeger",
    version=package_version,
    author="Joey Greco",
    author_email="joeyagreco@gmail.com",
    description="Instant stats for your fantasy football league.",
    long_description_content_type="text/markdown",
    long_description=readme,
    license="MIT",
    url="https://github.com/joeyagreco/leeger",
    packages=setuptools.find_packages(exclude=("test", "docs")),
    install_requires=["numpy",
                      "setuptools",
                      "openpyxl",
                      "espn-api",
                      "yahoofantasy",
                      "sleeper",
                      "pymfl"],
    python_requires=f">={minimum_python_version_required}",
    keywords="nfl statistics stats football espn yahoo sleeper myfantasyleague"
)
