# Gitools

![PyPI](https://img.shields.io/pypi/v/Gitools?style=for-the-badge)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://github.com/AliRezaBeigy/Gitools/blob/master/LICENSE)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)
![GitHub Repo stars](https://img.shields.io/github/stars/AliRezaBeigy/Gitools?style=for-the-badge)

A handy tool to modify git history

# Quick Start

You need to install python to use this app, so you can simply download python from [Official Site](https://www.python.org/downloads)

Now you should install Gitools as global app:

```shell
$ pip install -U Gitools
or
$ python -m pip install -U Gitools
```

# Usage

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

```shell
$ gitools -h
usage: gitools [-h] [-c COUNT] [-d DATE] [-ch HASH] [-m MODE]

optional arguments:
  -h        --help          show this help message and exit
  -c        --count         number of commit to show
  -d        --date DATE
  -ch       --hash HASH     commit hash
  -m        --mode MODE
```

# Features

- Modify Commit Message
- Modify Commit Date Time

# Contributions

This project is based on git filter-branch. As [indygreg](https://twitter.com/indygreg) calls it "the swiss-army knife of Git history rewriting".

If you're interested in contributing to this project, first of all I would like to extend my heartfelt gratitude.

Please feel free to reach out to me if you need help. My Email: AliRezaBeigyKhu@gmail.com
Telegram: [@AliRezaBeigy](https://t.me/AliRezaBeigyKhu)

# LICENSE

MIT
