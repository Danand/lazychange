# Lazy Change

Scripts for really lazy comitters.

## How to install

```bash
pip install git+https://github.com/Danand/lazychange.git
```

## How to use

### Bump

Automates the process of committing changes by utilizing **ChatGPT** for creating meaningful commit messages. Specifically, it performs the following steps:

1. Retrieves `git diff` to describe changes via **ChatGPT** for the commit message.
2. Commits the changes.
3. Pushes the commit.

#### With tag

Bumps and pushes the Git tag using **ChatGPT**, automatically determining the tagging style from the existing Git repository:

```bash
lazychange bump --tags
```

#### Without tag

Automatically commits and pushes changes without bumping the Git tag:

```bash
lazychange bump
```
