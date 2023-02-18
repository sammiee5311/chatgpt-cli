from setuptools import find_packages, setup

dev_requires = [
    "pytest",
    "pytest-cov"
    "pytest-env",
    "black",
    "mypy",
    "isort",
    "tox",
    ]

if __name__ == "__main__":
    setup(
        name="chatpg",
        author="sammiee5311",
        author_email="sammiee5311@gmail.com",
        description="description",
        packages=find_packages(exclude=("tests")),
        install_requires=[],
        extras_require={"dev": dev_requires},
    )
