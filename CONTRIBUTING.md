# Contributing

This project adheres to openZIM's [Contribution Guidelines](https://github.com/openzim/overview/wiki/Contributing)
and openZIM's [Bootstrap conventions](https://github.com/openzim/_python-bootstrap/wiki/) especially its
[Policy](https://github.com/openzim/_python-bootstrap/wiki/Policy).

## Guidelines

- Don't take assigned issues. Comment if those get staled.
- If your contribution is far from trivial, open an issue to discuss it first.
- Ensure your code passes `inv lintall` and `inv checkall`

## Configure your environment

Development environment is meant to be managed by `hatch` and commits can be checked with `pre-commit`.

If not already installed on your machine, install it in your global environment:

```
pip install -U hatch pre-commit
```

Install precommit

```
pre-commit install
```

Go to scraper directory:

```
cd scraper
```

Start a hatch shell to run further commands:

```
hatch shell
```

Install/Update dependencies:

```sh
pip install -U ".[dev]"
```
