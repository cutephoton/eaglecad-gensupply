# eaglecad-gensupply

This is a simple script to generate an Eagle CAD library containing supply symbols.
Basically I got tired of making the cumbersome supply symbols. As with most
exceptionally amazing ideas an engineer like myself would think up, it took more
time to write this code than it would have by hand.

Nevertheless, it works and hopefully any person daring to run this will find it
solves the problem quickly for them too.

Alternatively file an issue on github to explain how I could have saved myself
an hour or two had I been more competent using Eagle.

```
usage: eagle-gensupply.py [-h] [--out OUT] [--debug] [--force] [--mkdir] config

Creates an Eagle CAD supply library.

positional arguments:
  config      A JSON file containing a description of the supplies.

optional arguments:
  -h, --help  show this help message and exit
  --out OUT   Path to output directory. May be specified in json. If not specified in either, defaults to '~/EAGLE/libraries'.
  --debug     Enable debug logs.
  --force     Overwrite files if they already exist.
  --mkdir     Create directory if needed.

=== Example: Supply File Example ===

eagle-gensupply.py --in example.json --out path/to/output

example.json
>>  {
>>      "prefix" : "sup2_",               // Optional
>>      "output" : "~/EAGLE/lbr/",        // Optional
>>      "groups" : {
>>          "symbolic" : {
>>              "title" : "Supply: Symbolic",
>>              "supplies": [
>>                  {"name":"Gnd",      "style":"F-"},
>>                  {"name":"Vdd",      "style":"F+"},
>>                  {"name":"Vcc",      "style":"F+"},
>>                  {"name":"Vee",      "style":"F-"},
>>                  {"name":"Vss",      "style":"F-"}
>>              ]
>>          },
>>          "absolute": {
>>              "title" : "Supply: Absolute Common",
>>              "supplies": [
>>                  {"name":"+3V3",       "style":"F+"},
>>                  {"name":"+5V",        "style":"F+"},
>>                  {"name":"-3V3",       "style":"F-"},
>>                  {"name":"-5V",        "style":"F-"}
>>              ]
>>          },
>>      }
>>  }

=== Available Styles ===
   0) ARROW1+              (aliases: A1, A, A+, A1+)
   1) ARROW1+:HALF         (aliases: A1:HALF, A1+:HALF, A1H, A1+H, A1:H, A1+:H, ARROW1+H)
   2) ARROW1-              (aliases: A1-)
   3) ARROW1-:HALF         (aliases: A1-:HALF, A1-H, A1-:H, ARROW1-H)
   4) ARROW2+              (aliases: A2, A2+)
   5) ARROW2+:HALF         (aliases: A2:HALF, A2+:HALF, A2H, A2:H, A2+H, A2+:H, ARROW2+H, ARROW2+:H)
   6) ARROW2-              (aliases: A2-)
   7) ARROW2-:HALF         (aliases: A2-:HALF, A2-H, A2-:H, ARROW2-H)
   8) ARROW3+              (aliases: A3, A3+)
   9) ARROW3+:HALF         (aliases: A3:HALF, A3+:HALF, A3H, A3+H, A3:H, A3+:H, ARROW3+H, ARROW3+:H)
  10) ARROW3-              (aliases: A3-)
  11) ARROW3-:HALF         (aliases: A3-:HALF, A3-H, A3-:H, ARROW3-H)
  12) COMMON               (aliases: COM)
  13) FLAT:DOWN            (aliases: FLAT-, F-)
  14) FLAT:UP              (aliases: FLAT+, F+, FLAT)
  15) GND1                 (aliases: G, G1, GND, 0)
  16) GND2                 (aliases: G2)
  17) GND2:DASH            (aliases: G2D, G3:D, G2:DASH, GND2D)
  18) GND3                 (aliases: G3)
  19) GND3:DASH            (aliases: G3D, G3:D, G3:DASH, GND3D)
  20) GND4                 (aliases: G4)
  21) TRIANGLE+            (aliases: +, T1+, T1)
  22) TRIANGLE-            (aliases: -, T1-)
  23) TRIANGLE2+           (aliases: T2+, T2)
  24) TRIANGLE2-           (aliases: T2-)

=== Developer ===

Author:       Brett Foster <fosterb@cutephoton.com>
Web:          https://www.cutephoton.com/
URL:          https://github.com/cutephoton/eaglecad-gensupply

```
