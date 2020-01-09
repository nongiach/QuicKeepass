# QuicKeepass
QuicKeepass is a tool that allows you to quickly paste password from your Keepass database using keyboard shorcuts.

| Video DEMO: How to use QuicKeepass | Video Install and Configure QuicKeepass |
|----------|:-------------:|
| [![ DEMO: How to use QuicKeepass](https://img.youtube.com/vi/1gRADHlXerM/0.jpg)](https://www.youtube.com/watch?v=1gRADHlXerM) | [![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/R2L0lEDUhGE/0.jpg)](https://www.youtube.com/watch?v=R2L0lEDUhGE) |

# How to use
* Type <Alt+u> to start QuicKeepass
* Enter your keepass Master Passwod
* Type <Enter> to Autofill username and password

## Keyboard shortcuts

* $mod+u      =>      Start QuicKeepass
* Enter       =>      Autofill username and password
* Alt+Enter   =>      Autofill type password only

## How to install
```sh
$ sudo pip3 install quickeepass
```

## How to use
```bash
$ quickeepass REPLACE_WITH_YOUR_KEEPASS.kdbx
$ # or
$ quickeepass REPLACE_WITH_YOUR_KEEPASS.kdbx --keyfile your.key
$ # or
$ quickeepass REPLACE_WITH_YOUR_KEEPASS.kdbx --keyfile your.key --password
```

## How to configure

Add one of the bellow lines to your ~/.config/i3/config

### i3 Basic configuration
```
bindsym $mod+u exec "quickeepass REPLACE_WITH_YOUR_KEEPASS.kdbx"
```

### Rofi theme
Add the bellow arguments to change the theme.

```quickeepass --rofiargs '-theme purple' test/password_only.kdbx```

List of available theme like solarized [here](https://github.com/davatorium/rofi-themes/tree/master/Official%20Themes)

### Rofi activate fuzzy matching
Please man rofi to go deeper.

```quickeepass --rofiargs '-matching fuzzy' test/password_only.kdbx```

### For other Window manager

This should work perfectly, just see the above commands and adapt the start command, pull requests are welcom.


## Warning
QuicKeepass is not a replacement to Keepass it only wraps Keepass to allow you to efficiently paste your passwords on Linux.

## New features?
* Tell me what you need :)
* Maybe we will remember the required password using the windows title..

----
By [@chaignc][] [#HexpressoTeam][hexpresso].


[hexpresso]:     https://hexpresso.github.io
[@chaignc]:    https://twitter.com/chaignc
