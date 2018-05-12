#!/usr/bin/python3
import json
import argparse
import sys
from io import StringIO
import html

COMMAND_DOC_EXAMPLES="""
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
"""

COMMAND_DOC_INFO="""
=== Developer ===

Author:       Brett Foster <fosterb@cutephoton.com>
Web:          https://www.cutephoton.com/
URL:          https://github.com/cutephoton/eaglecad-gensupply
"""

FILE_TEMPLATE="""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.0.0">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting keepoldvectorfont="yes"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.025" unitdist="inch" unit="inch" style="lines" multiple="1" display="yes" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="yes" active="yes"/>
<layer number="2" name="Route2" color="1" fill="3" visible="no" active="yes"/>
<layer number="3" name="Route3" color="4" fill="3" visible="no" active="yes"/>
<layer number="4" name="Route4" color="1" fill="4" visible="no" active="yes"/>
<layer number="5" name="Route5" color="4" fill="4" visible="no" active="yes"/>
<layer number="6" name="Route6" color="1" fill="8" visible="no" active="yes"/>
<layer number="7" name="Route7" color="4" fill="8" visible="no" active="yes"/>
<layer number="8" name="Route8" color="1" fill="2" visible="no" active="yes"/>
<layer number="9" name="Route9" color="4" fill="2" visible="no" active="yes"/>
<layer number="10" name="Route10" color="1" fill="7" visible="no" active="yes"/>
<layer number="11" name="Route11" color="4" fill="7" visible="no" active="yes"/>
<layer number="12" name="Route12" color="1" fill="5" visible="no" active="yes"/>
<layer number="13" name="Route13" color="4" fill="5" visible="no" active="yes"/>
<layer number="14" name="Route14" color="1" fill="6" visible="no" active="yes"/>
<layer number="15" name="Route15" color="4" fill="6" visible="no" active="yes"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="yes" active="yes"/>
<layer number="17" name="Pads" color="2" fill="1" visible="yes" active="yes"/>
<layer number="18" name="Vias" color="2" fill="1" visible="yes" active="yes"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="yes" active="yes"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="yes" active="yes"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="yes" active="yes"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="yes" active="yes"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="yes" active="yes"/>
<layer number="25" name="tNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="26" name="bNames" color="7" fill="1" visible="yes" active="yes"/>
<layer number="27" name="tValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="28" name="bValues" color="7" fill="1" visible="yes" active="yes"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="yes"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="yes"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="yes"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="yes"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="yes"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="yes"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="yes"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="yes"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="yes"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="yes"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="yes" active="yes"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="yes" active="yes"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="yes" active="yes"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="yes" active="yes"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="yes" active="yes"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="yes"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="yes"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="yes"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="yes"/>
<layer number="48" name="Document" color="7" fill="1" visible="yes" active="yes"/>
<layer number="49" name="Reference" color="7" fill="1" visible="yes" active="yes"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="yes" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<library>
<description>
&lt;b&gt;{title_esc}&lt;/b&gt;
&lt;ul&gt;
    {items}
&lt;/ul&gt;
&lt;p&gt;Generated using &lt;a href="https://github.com/cutephoton/eaglecad-gensupply"&gt;
eaglecad-gensupply.&lt;/a&gt;&lt;p&gt;
</description>
<packages>
</packages>
<symbols>
{symbols}
</symbols>
<devicesets>
{devices}
</devicesets>
</library>
</drawing>
</eagle>
"""

SUPPLY_DEV_TEMPLATE="""
    <deviceset name="{supply}" prefix="P+">
    <description>&lt;b&gt;SUPPLY SYMBOL&lt;/b&gt; {supply_esc}</description>
    <gates>
    <gate name="G$1" symbol="{supply}" x="0" y="0"/>
    </gates>
    <devices>
    <device name="">
    <technologies>
    <technology name=""/>
    </technologies>
    </device>
    </devices>
    </deviceset>
"""

SUPPLY_SYM_TEMPLATES = {
    "arrow3+" : """
        <symbol name="{supply}">
        <wire x1="0.889" y1="-1.27" x2="0" y2="0.127" width="0.254" layer="94"/>
        <wire x1="0" y1="0.127" x2="-0.889" y2="-1.27" width="0.254" layer="94"/>
        <wire x1="-0.889" y1="-1.27" x2="0.889" y2="-1.27" width="0.254" layer="94"/>
        <text x="0" y="1.27" size="1.778" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        </symbol>""",
    "arrow3-" : """
        <symbol name="{supply}">
        <wire x1="-0.889" y1="1.27" x2="0" y2="-0.127" width="0.254" layer="94"/>
        <wire x1="0" y1="-0.127" x2="0.889" y2="1.27" width="0.254" layer="94"/>
        <wire x1="-0.889" y1="1.27" x2="0.889" y2="1.27" width="0.254" layer="94"/>
        <text x="0" y="-1.27" size="1.778" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "split-arrow3" : """
        <symbol name="{supply}">
        <wire x1="2.54" y1="-0.889" x2="3.937" y2="0" width="0.254" layer="94"/>
        <wire x1="3.937" y1="0" x2="2.54" y2="0.889" width="0.254" layer="94"/>
        <wire x1="2.54" y1="0.889" x2="2.54" y2="0" width="0.254" layer="94"/>
        <text x="-5.08" y="1.27" size="1.778" layer="96">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        <wire x1="2.54" y1="0" x2="2.54" y2="-0.889" width="0.254" layer="94"/>
        <wire x1="-2.54" y1="0.889" x2="-3.937" y2="0" width="0.254" layer="94"/>
        <wire x1="-3.937" y1="0" x2="-2.54" y2="-0.889" width="0.254" layer="94"/>
        <wire x1="-2.54" y1="-0.889" x2="-2.54" y2="0" width="0.254" layer="94"/>
        <wire x1="-2.54" y1="0" x2="-2.54" y2="0.889" width="0.254" layer="94"/>
        <wire x1="-2.54" y1="0" x2="2.54" y2="0" width="0.254" layer="94" style="shortdash"/>
        </symbol>
    """,
    "arrow2+" : """
        <symbol name="{supply}">
        <wire x1="1.27" y1="-1.905" x2="0" y2="0" width="0.254" layer="94"/>
        <wire x1="0" y1="0" x2="-1.27" y2="-1.905" width="0.254" layer="94"/>
        <text x="0" y="1.27" size="1.778" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        </symbol>
    """,
    "arrow2-" : """
        <symbol name="{supply}">
        <wire x1="-1.27" y1="1.905" x2="0" y2="0" width="0.254" layer="94"/>
        <wire x1="0" y1="0" x2="1.27" y2="1.905" width="0.254" layer="94"/>
        <text x="0" y="-1.27" size="1.778" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "gnd_flat" : """
        <symbol name="{supply}">
        <wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.254" layer="94"/>
        <text x="0" y="-1.27" size="1.778" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "gnd_double" : """
        <symbol name="{supply}">
        <wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.254" layer="94"/>
        <wire x1="-1.0922" y1="-0.508" x2="1.0922" y2="-0.508" width="0.254" layer="94"/>
        <text x="0" y="-1.905" size="1.778" layer="96" rot="R180" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """
}

COMMAND_DOC_STYLES="""
=== Available Styles ===
{styles}
""".format(styles="".join(["  {}) {:20s}\n".format(idx,i) for idx,i in enumerate(sorted(SUPPLY_SYM_TEMPLATES.keys()))]))

SUPPLY_SYM_TEMPLATES["g"] = SUPPLY_SYM_TEMPLATES["gnd_flat"]
SUPPLY_SYM_TEMPLATES["+"] = SUPPLY_SYM_TEMPLATES["arrow3+"]
SUPPLY_SYM_TEMPLATES["-"] = SUPPLY_SYM_TEMPLATES["arrow3-"]

COMMAND_DOC=COMMAND_DOC_EXAMPLES+COMMAND_DOC_STYLES+COMMAND_DOC_INFO

supplies = {}
out_params = {
    "items" : "",
    "title" : ""
}

def escape (esc,dbl=False):
    if dbl:
        return html.escape(html.escape(esc))
    else:
        return html.escape(esc)

def autostyle(name):
    name = name.lower()
    if (name.startswith("gnd")):
        return "g"
    if (name.startswith("+") or name.endswith("+")):
        return "+"
    if (name.startswith("-") or name.endswith("-")):
        return "-"
    return "+"

def mksupply(idx, sup_name, sup_style = None):
    if sup_name is None or len(sup_name) == 0:
        sys.stderr.write ("[Supply #{}] **ERROR** Supply has no name.\n".format(idx+1))
        return False
    sup_name = sup_name.upper()

    if ':' in sup_name or ';' in sup_name:
        sys.stderr.write ("[Supply {} #{}] **ERROR** Supply name has invalid characters.\n".format(sup_name,idx+1))
        return False

    if sup_name in supplies:
        sys.stderr.write ("[Supply {} #{}] **ERROR** Already exists.\n".format(sup_name, idx+1))
        return False

    if sup_style is None:
        sup_style=autostyle(sup_name)
        sys.stderr.write ("[Supply {} #{}] Adding with default style '{}'.\n".format(sup_name,idx+1,sup_style))
    elif sup_style not in SUPPLY_SYM_TEMPLATES:
        sup_style_tmp=autostyle(sup_name)
        sys.stderr.write ("[Supply {} #{}] **ERROR** Style '{}' missing. Adding with '{}' instead.\n".format(sup_name,idx+1,sup_style,sup_style_tmp))
        sup_style=sup_style_tmp
    else:
        sys.stderr.write ("[Supply {} #{}] Added with style '{}'\n".format(sup_name,idx+1,sup_style))
    supplies[sup_name] = (sup_name, sup_style)

    return True

parser = argparse.ArgumentParser(description='Creates an Eagle CAD supply library.', formatter_class=argparse.RawTextHelpFormatter, epilog=(COMMAND_DOC))
parser.add_argument('--add-supply', action='append',
help='''Creates a supply to add to the library. Most characters valid except ';' and ':'.
The argument is in the form 'SUPPLY[:style]'. Style is optional.
Use --add-supply=-X for negative supplies.''')

parser.add_argument('--supplies', type=argparse.FileType('r'), help="A JSON file containing a description of the supplies.")
parser.add_argument('--output', type=argparse.FileType('w'), help="The output file. If not specified, use stdout.")
parser.add_argument('--title', default="Supplies", help="Sets a title in the resulting library.")
args = parser.parse_args()
validated = True

if (args.add_supply is None and args.supplies is None):
    parser.error("Provide --add-supply or --supplies argument.")

out_params['title'] = args.title

if args.supplies is not None:
    conf = json.load(args.supplies)

    if "title" in conf:
        out_params['title'] = conf["title"]

    if "supplies" in conf:
        if isinstance(conf["supplies"], list):
            if len(conf["supplies"]) == 0:
                sys.stderr.write ("[Error] No supplies defined in the configuration file.\n")
                validated = False
            else:
                for idx, i in enumerate(conf["supplies"]):
                    if "name" not in i:
                        sys.stderr.write ("[Supply (unnamed) #{}] **ERROR** Supply has no name.\n".format(idx))
                        validated = False
                        continue
                    validated = validated and mksupply(idx, i["name"], i["style"] if "style" in i else None)
        else:
            sys.stderr.write ("[Error] Supply configuration section 'supplies' is not an array.\n")
            validated = False
    else:
        sys.stderr.write ("[Error] No supplies section in configuration file.\n")
        validated = False

if args.add_supply is not None:
    for idx, i in enumerate(args.add_supply):
        supply_raw = i.split(':',2)
        if supply_raw[0].startswith("|"):
            supply_raw[0] = supply_raw[0][1:]
        validated = validated and mksupply(idx, *supply_raw)

if not validated:
    sys.stderr.write ("[Error] Unable to generate supply library. Fix error above.\n")
    sys.exit(1)

if len(supplies) < 1:
    sys.stderr.write ("[Info] No supplies generated.\n")
    sys.exit(1)

out_params['items'] = "".join(["&lt;li&gt;" + escape(i, True) + "&lt;/li&gt;" for i in supplies.keys()])
out_params['title'] = out_params['title']
out_params['title_esc'] = escape(out_params['title'], True)
symbols = StringIO()
devices = StringIO()
for k,v in supplies.items():
    sup_name = v[0]
    sup_name_esc=escape(sup_name)
    sup_name_esc2=escape(sup_name, True)
    sup_style = v[1]
    sup_style_template = SUPPLY_SYM_TEMPLATES[sup_style]

    sys.stderr.write ("[Supply {}] Generating.\n".format(sup_name))

    symbols.write(sup_style_template.format(supply=sup_name_esc,supply_esc=sup_name_esc2))
    devices.write(SUPPLY_DEV_TEMPLATE.format(supply=sup_name_esc,supply_esc=sup_name_esc2))

out = sys.stdout if args.output is None else args.output
out.write(FILE_TEMPLATE.format(symbols=symbols.getvalue(),devices=devices.getvalue(), **out_params))
