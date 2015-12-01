Ansibrew
========

A simple command-line tool to generate vars of Ansible playbook for Homebrew.

## Installation

```
$ pip install git+https://github.com/takuti/ansibrew.git
```

## Usage

### taps

```
$ ansibrew taps
```

- `brew tap`

### packages

```
$ ansibrew packages
```

- `brew list`
- except all required packages because they will be installed automatically as dependencies

### cask

```
$ ansibrew cask
```

- search by `brew cask search` for all applications in */Applications* directory

## License

MIT

## Reference

- [twada/macbook-provisioning](https://github.com/twada/macbook-provisioning)