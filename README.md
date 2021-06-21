# Gitools

![PyPI](https://img.shields.io/pypi/v/Gitools?style=for-the-badge)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://github.com/AliRezaBeigy/Gitools/blob/master/LICENSE)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)
![GitHub Repo stars](https://img.shields.io/github/stars/AliRezaBeigy/Gitools?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/gitools?style=for-the-badge)

A handy tool to modify git history

<p align="center">
  <img width="1350" src="https://raw.githubusercontent.com/AliRezaBeigy/Gitools/master/asciinema.svg">
</p>

## Requirement

- Python 3

- Knowing following rule:
  - **Do not change a shared history**

## Quick Start

You need to install python to use this app, so you can simply download python from [Official Site](https://www.python.org/downloads)

Now you should install Gitools as global app:

```shell
$ pip install -U Gitools
or
$ python -m pip install -U Gitools
```

**Use `-U` option to update Gitools to the last version**

:warning: **Do not change a shared history**

## Usage

```shell
$ gitools

$ gitools -c [commit_count]
```

Example:

```shell
$ gitools -c 100

$ gitools -ch ca895a914fc551f50301b83311c803846454bc21
```

For more details:

```text
$ gitools -h
usage: gitools [-h] [-c COUNT] [-an AUTHOR_NAME] [-ae AUTHOR_EMAIL] [-cd COMMIT_DATE]
                     [-ch COMMIT_HASH] [-cm COMMIT_MESSAGE] [-m MODE] [-i INPUT]

optional arguments:
  -h        --help                 show this help message and exit
  -c        --count                number of commit to show
  -cm       --commit-message       commit message
  -ae       --author-email         author email
  -an       --author-name          author name
  -cd       --commit-date          commit date
  -ch       --commit-hash          commit hash
  -i        --input                git directory
  -m        --module               select module to do something
```

## Features

- Modify Commit Author
- Modify Commit Message
- Modify Commit Date Time

## Contributions

This project is based on git filter-branch. As [indygreg](https://twitter.com/indygreg) calls it "the swiss-army knife of Git history rewriting".

If you're interested in contributing to this project, first of all I would like to extend my heartfelt gratitude.

Please feel free to reach out to me if you need help. My Email: AliRezaBeigyKhu@gmail.com
Telegram: [@AliRezaBeigy](https://t.me/AliRezaBeigyKhu)

## LICENSE

MIT
