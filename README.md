# chatgpt-cli (0.1.1)

[![CI](https://github.com/sammiee5311/chatpg/actions/workflows/CI.yaml/badge.svg)](https://github.com/sammiee5311/chatpg/actions/workflows/CI.yaml) [![python](./imgs/python-version.svg)]() [![](./imgs/coverage.svg?dummy=8484744)]()

ChatGPT cli version with history.

# How to use
- Install `ffmpeg` if you didn't install it on your machine.
- Create a virtualenv (Optional)
- Use `pip install -r requirements.txt` command to install the dependencies.
- Check `python main.py --help` for more detailed arguments
- Use `python main.py <args>` to run the ChatGPT-cli.

# Pre-requisites
- <= python 3.8
- ffmpeg

# Setup Environment
- Dev
    - Run `make setup-dev-chatpg`
- Prod
    - Run `make setup-chatpg`

# Features
- Voice assistant
    - You can hear the answer of the question by voice.
- History
    - You can save history what you were asking and the answer from ChatGPT.
    - Only working properly with `Turbo` model and `paid` version, currently.
    - The history data will be stored in `history.sqlite3`.
- continuous / single
    - You can ask multiple questions or single question.
- models
    - You can choose models which are proviced from ChatGPT.
        - turbo
        - davinci
        - curie
        - babbage
        - ada

# Arguments
- `--con`
    - Ask continuous questions to ChatGPT (Default: `Single`).
    - example
        - ```python main.py --con```
- `--paid`
    - Use paid version (Default: `Free`).
    - example
        - ```python main.py --paid```
- `-m` / `--model`
    - Please choose one of the provided models (Default: `Turbo`).
    - Provided models
        - turbo
        - davinci
        - curie
        - babbage
        - ada
    - example
        - ```python main.py -m davinci```
- `--voice`
    - Enable voice assistant (Default: `disabled`)
    - example
        - ```python main.py --voice```

# Test
- Pytest
    - Run `make test-ci-chatpg`
- Tox
    - To run tox, python versions in the default setting are `3.8`, `3.9`, and `3.10`. You can configure the python versions in `tox.ini` file.
    - Run `make test-chatpg`
