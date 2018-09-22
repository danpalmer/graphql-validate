"""Package setup."""

import version
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="graphql-validate",
    version=version.get_version(),
    url="https://github.com/danpalmer/graphql-validate",
    description="GraphQL API Validation toolkit.",
    long_description=long_description,
    author="Dan Palmer",
    author_email="dan@danpalmer.me",
    keywords=("graphql",),
    license="MIT",
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    classifiers=(
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
    ),
    install_requires=("graphql-core-next", "click", "requests"),
    setup_requires=("pytest-runner",),
    tests_require=("pytest", "networkx", "tox", "pytest-cov", "pytest-pythonpath"),
    entry_points={"console_scripts": ("graphql-validate = graphql_validate.cli:cli",)},
)
