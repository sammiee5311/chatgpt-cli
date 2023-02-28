# chatpg

[![CI](https://github.com/sammiee5311/chatpg/actions/workflows/CI.yaml/badge.svg)](https://github.com/sammiee5311/chatpg/actions/workflows/CI.yaml) [![python](./imgs/python-version.svg)]() [![](./imgs/coverage.svg?dummy=8484744)]()

## prerequisites
- <= python 3.8

# Setup Environment
- Dev
    - Run `make setup-dev-chatpg`
- Prod
    - Run `make setup-chatpg`

# Test
- Pytest
    - Run `make test-ci-chatpg`
- Tox
    - To run tox, python versions in the default setting are `3.8`, `3.9`, and `3.10`. You can configure the python versions in `tox.ini` file.
    - Run `make test-chatpg`
