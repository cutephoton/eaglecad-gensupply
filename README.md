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
usage: eagle-gensupply.py [-h] [--add-supply ADD_SUPPLY] [--supplies SUPPLIES]
                          [--output OUTPUT] [--title TITLE]

Creates an Eagle CAD supply library.

optional arguments:
  -h, --help            show this help message and exit
  --add-supply ADD_SUPPLY
                        Creates a supply to add to the library. Most characters valid except ';' and ':'.
                        The argument is in the form 'SUPPLY[:style]'. Style is optional.
                        Use --add-supply=-X for negative supplies.
  --supplies SUPPLIES   A JSON file containing a description of the supplies.
  --output OUTPUT       The output file. If not specified, use stdout.
  --title TITLE         Sets a title in the resulting library.

=== Example: Supplies as a configuration file ===

eagle-gensupply.py --supplies example.json --output example.lbr

example.json
>>  {
>>      "title" : "My Library Title",
>>      "supplies" : [
>>          {"name":"VSupply+", "style":"StyleName1"},
>>          {"name":"VSupply-", "style":"StyleName2"},
>>          {"name":"VSupply-"}
>>      ]
>>  }

=== Example: Supplies as Arguments ===

eagle-gensupply.py --add-supply "+5V:+" --add-supply "|-5V:-"
                   --add-supply="-12V" --add-supply="+12V"
                   --output test.lbr

=== Available Styles ===
  0) arrow2+             
  1) arrow2-             
  2) arrow3+             
  3) arrow3-             
  4) gnd_double          
  5) gnd_flat            
  6) split-arrow3        

=== Developer ===

Author:       Brett Foster <fosterb@cutephoton.com>
Web:          https://www.cutephoton.com/
URL:          https://github.com/cutephoton/eaglecad-gensupply
```
