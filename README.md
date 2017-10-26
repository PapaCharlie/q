# `q`uick links

Like LinkedIn's go links, which resolve to different shortcuts like `go/wiki` or `go/git`, I wanted to be able to quickly hop to websites in a more reliable way than Chrome's autocomplete from history, hence `q` links. These short links will redirect you to specific places with probably very long URLs, but are distinctly more memorable. To do this, we can run a small server that reads the shortcuts from a file and redirects the user to wherever they please!

## Instalation (MacOS and Linux only, Windows TBD)

### Requirments

Installing is easy, all you need is `sudo` access on the machine you're trying to install this on and have the following Python packages installed:

+ `gunicorn`
+ `filelock`
+ `PyYAML`

You will also need `make` installed, but it should be installed by default on all Linux distributions and after installing the command line utils on MacOS.

### Setup

Once you've installed all the requirments, add the following line to your `/etc/hosts` file (requires `sudo`):

```
127.0.1.2 q
```

This will resolve the `q` TLD to you local IP `127.0.1.2`. On MacOS, you will need to set up an alias on the loopback interface, which you can do by running:
```bash
make loopback-alias
```

### Running `q`

It's as simple as running `make` in the install directory!

## Usage

Once `q` is running, all you need to do navigate to `q/{your/shortcut/here}` from your browser. If it doesn't work right away, you may need to force your browser to cache the resolution as an actual domain rather than a query by browsing to `https://q/{your/shortcut/here}`. You may also use the `q` script included in this repository, which will let you open the shortcuts directly from the command line.

### Creating a shortcuts file

The default location for your shortcuts is `~/.q.yaml`. The syntax is plain YAML, and may look a little like this:

```yaml
aws:
  '*': https://console.aws.amazon.com/
  dns: 'https://console.aws.amazon.com/route53/home?#hosted-zones:'
  repo: https://console.aws.amazon.com/ecs/home#/repositories
mail: https://mail.google.com/mail/u/0/#inbox
```

As you can see, you can have arbitrarily nested maps. To open the `dns` shortcut, which will take you to the Route53 dashboard, you should navigate to `q/aws/dns`. The `'*'` entry is the default entry, and `q/aws` will point to that entry. You can edit this file manually, or you can add a new shortcut automatically through the browser. For example, suppose you loved this project so much you wanted to get to it as quickly and as efficiently as possible. You may want to map `q/git/q` to `https://github.com/PapaCharlie/q`. You can add an entry like this to your shortcuts file:

```yaml
git:
  q: https://github.com/PapaCharlie/q
```

Or you can just navigate to `q/ git/q https://github.com/PapaCharlie/q`. What's nice here is that you can save the current location in your browser by prepending `q/ {shortcut}` to the current url in your address bar, all without leaving your keyboard. Easy as pie!



