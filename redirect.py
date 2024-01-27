#!/usr/bin/python3
import sys

print("""
<!doctype HTML>
<html>
    <head>
        <title>Redirecting to {dest}</title>
        <meta http-equiv="Refresh" content="0; url='{dest}'" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
    </head>
</html>
""".format(dest=sys.argv[1]))
