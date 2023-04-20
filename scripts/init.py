if __name__ == "__main__":
    import sys
    from pathlib import Path

    args = sys.argv[1:]
    if len(args) < 2:
        raise ValueError("Expected two arguments: '<repo>' '<description>'")

    repo, description = args

    Path("pyproject.toml").write_text(f"""\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{repo}"
version = "0.1.0"
description = "{description}"
readme = "README.md"
license = "MIT"
authors = [
    {{ name="Tired Fox", email="zboehm104@gmail.com"}}
]
classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
]
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
tests = [
  "pytest",
  "pytest-cov"
]
dev = [
  "black",
  "ruff",
  "requests"
]

[project.urls]
"Homepage" = "https://github.com/Tired-Fox/{repo}"
"Website" = "https://tired-fox.github.io/{repo}/"

[project.scripts]

[tool.ruff]
ignore = [
  "ANN101"
]
extend-select = [
    'E',
    'F',
    'W',
    "C90",
    "I",
    "N",
    "UP",
    "ANN",
    "S",
    "A",
    "B",
    "COM",
    "C4",
    "Q",
    "RET",
    "SIM",
    "TCH",
    "PTH",
    "PLE",
    "RUF"
]
""")

    Path("Makefile").write_text(f"""\
PROJECT = {repo}

init:
	pip3 install -e .[]
install:
	pip3 install -e .

all:
	make install format lint

format:
	ruff check --fix-only && black $(PROJECT)

lint:
	ruff check ./$(PROJECT)

statistics:
	ruff check --statistics ./$(PROJECT)

type:
	mypy $(PROJECT)

# Testing

test:
	pytest --cov="./$(PROJECT)" tests/

cover:
	coverage html

open:
	python cover.py

test-cov:
	make test cover

# Built/Deploy

build_docs:
	pdoc $(PROJECT) -d google -o docs/

badges:
	python scripts/make_badges.py

build:
	make badges
	python -m build

deploy:
	python -m twine upload --repository pypi dist/*

build_deploy:
	make build deploy
"""
)
    # pInit.parent.mkdir(exist_ok=True, parents=True)
    Path(f"{repo}/__init__.py").write_text("")