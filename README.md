# twitter_osint

Perform "OSINT-y" actions using the Twitter API.

Built upon my [twitter_api](https://github.com/vphpersson/twitter_api) library. The actions defined in its CLI component are used as fallbacks, and can thus also be used via this program.

## Actions

### intersection

Output the names of accounts that follow a specified account, who the specified account also follows.

NOTE: Running this against an account with a lot of followers will result in a "429 Too Many Requests" error, unfortunately.

Example invocation:
```shell
$ ./twitter_osint.py "$CONSUMER_KEY" "$CONSUMER_SECRET" intersection --screen-name 'terjanq'
```

Output (truncated):
```
...
the_st0rm
pawel_lukasik
mikispag
LiveOverflow
sakiirsecurity
ret2jazzy
shafigullin
st98_
zwad3
```

### creation

Output the creation date of a specified account, exactly as received from the API response.

Example invocation:
```shell
$ ./twitter_osint.py "$CONSUMER_KEY" "$CONSUMER_SECRET" creation --screen-name 'MagnusCarlsen'
```

Output:
```
Sat Apr 11 00:28:29 +0000 2009
```

### first_followers

Output information about the first five  still-existing accounts that followed a specified account. Of note is the approximate follow date, which is calculated according to a formula with a to me inexplicable magic number (see the definition of the `cursor_id_to_datetime` function) and is thus not information obtained directly from the Twitter API.

Example invocation:
```shell
$ ./twitter_osint.py "$CONSUMER_KEY" "$CONSUMER_SECRET" first_followers --screen-name 'MagnusCarlsen'
```
Output:
```
Screen name     Name              Created                    ~Follow date
--------------  ----------------  -------------------------  --------------------------------
oyvindbrunvoll  Øyvind Brunvoll   2008-01-06 16:39:16+00:00  2009-04-15 12:39:54.006085+00:00
modchip1985     Fleetwood Dvorak  2009-04-25 01:06:38+00:00  2009-04-25 00:19:41.643144+00:00
magnetor        meg               2009-04-04 12:20:55+00:00  2009-05-04 16:29:28.579245+00:00
magnohr         Magnus Ohren      2009-05-06 00:28:12+00:00  2009-05-05 23:49:09.499180+00:00
oleval          Ole Valaker       2009-05-22 12:00:19+00:00  2009-05-22 17:35:52.542496+00:00
```
