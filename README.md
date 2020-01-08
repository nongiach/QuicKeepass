# QuicKeepass
QuicKeepass is a tool that allows you to quickly paste password from your Keepass database using keyboard shorcuts.

## Keyboard shortcuts

* $mod+u      =>      Start QuicKeepass
* Enter       =>      Autofill username and password
* Alt+Enter   =>      Autofill type password only

## How to install
```sh
$ sudo pip3 install quickeepass
```

## How to configure

Add one of the bellow lines to your ~/.config/i3/config

### i3 Basic configuration: Master Password
```
bindsym $mod+u exec "quickeepass REPLACE_WITH_YOUR_KEEPASS.kdbx"
```

### i3 Advanced configuration 1: Keyfile
```
bindsym $mod+u exec "quickeepass REPLACE_WITH_YOUR_KEEPASS.kdbx --keyfile your.key"
```

### i3 Advanced configuration 2: KeyFile and Password

```
bindsym $mod+u exec "quickeepass REPLACE_WITH_YOUR_KEEPASS.kdbx --keyfile your.key --password"
```

## Warning
QuicKeepass is not a replacement to Keepass it only wraps Keepass to allow you to efficiently paste your passwords on Linux.
