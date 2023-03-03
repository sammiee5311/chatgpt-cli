from setuptools import find_packages
from setuptools import setup

dev_requires = [
    "pytest",
    "pytest-cov",
    "pytest-env",
    "requests-mock",
    "black",
    "mypy",
    "isort",
    "tox",
    "httpx",
    "mock",
]

if __name__ == "__main__":
    setup(
        name="chatpg",
        author="sammiee5311",
        author_email="sammiee5311@gmail.com",
        description="description",
        packages=find_packages(exclude=("tests")),
        install_requires=[
            "python-dotenv",
            "openai",
        ],
        extras_require={"dev": dev_requires},
    )
