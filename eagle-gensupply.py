#!/usr/bin/env python3
import traceback
import json
import argparse
import sys
import os
import types
from collections.abc import Iterable
from itertools import chain
from io import StringIO
import html

COMMAND_DOC_EXAMPLES="""
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
    <description>&lt;b&gt;SUPPLY SYMBOL&lt;/b&gt; {supply_esc2}</description>
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

# Helper Regex to help transform symbols from eagle files:
# Rename Symbol
#               1      23                  45
# <symbol name="(.*?)">((.|\n)*?)name=".*?"((.|\n)*?)</symbol>
#     "\1" : """\n<symbol name="{supply}">\2name="{supply}"\4</symbol>\n""",
SUPPLY_SYM_TEMPLATES = {
    "TRIANGLE+" : """
        <symbol name="{supply}">
        <wire x1="0.889" y1="-1.27" x2="0" y2="0.127" width="0.15" layer="94"/>
        <wire x1="0" y1="0.127" x2="-0.889" y2="-1.27" width="0.15" layer="94"/>
        <wire x1="-0.889" y1="-1.27" x2="0.889" y2="-1.27" width="0.15" layer="94"/>
        <text x="0" y="1.27" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        </symbol>
    """,
    "COMMON" : """
    <symbol name="{supply}">
        <text x="0" y="-3.81" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="SUPPLY" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        <wire x1="0" y1="0" x2="-2.54" y2="0" width="0.254" layer="94"/>
        <wire x1="-2.54" y1="0" x2="-5.08" y2="-2.54" width="0.254" layer="94"/>
        <wire x1="-2.54" y1="-2.54" x2="0" y2="0" width="0.254" layer="94"/>
        <wire x1="0" y1="0" x2="2.54" y2="0" width="0.254" layer="94"/>
        <wire x1="2.54" y1="0" x2="0" y2="-2.54" width="0.254" layer="94"/>
    </symbol>
    """,
    "ARROW2+" : """
        <symbol name="{supply}">
        <wire x1="1.27" y1="-1.905" x2="0" y2="0" width="0.15" layer="94"/>
        <wire x1="0" y1="0" x2="-1.27" y2="-1.905" width="0.15" layer="94"/>
        <wire x1="1.27" y1="-0.635" x2="0" y2="1.27" width="0.15" layer="94"/>
        <wire x1="0" y1="1.27" x2="-1.27" y2="-0.635" width="0.15" layer="94"/>
        <text x="0" y="2.286" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        </symbol>
    """,
    "TRIANGLE-" : """
        <symbol name="{supply}">
        <wire x1="-0.889" y1="1.27" x2="0" y2="-0.127" width="0.15" layer="94"/>
        <wire x1="0" y1="-0.127" x2="0.889" y2="1.27" width="0.15" layer="94"/>
        <wire x1="-0.889" y1="1.27" x2="0.889" y2="1.27" width="0.15" layer="94"/>
        <text x="0" y="-1.27" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "ARROW2-" : """
        <symbol name="{supply}">
        <wire x1="-1.27" y1="1.905" x2="0" y2="0" width="0.15" layer="94"/>
        <wire x1="0" y1="0" x2="1.27" y2="1.905" width="0.15" layer="94"/>
        <wire x1="-1.27" y1="0.635" x2="0" y2="-1.27" width="0.15" layer="94"/>
        <wire x1="0" y1="-1.27" x2="1.27" y2="0.635" width="0.15" layer="94"/>
        <text x="0" y="-2.286" size="1.4" layer="96" rot="R180" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "GND1" : """
        <symbol name="{supply}">
        <wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.15" layer="94"/>
        <text x="0" y="-1.27" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "GND2" : """
        <symbol name="{supply}">
        <wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.15" layer="94"/>
        <wire x1="-1.0922" y1="-0.508" x2="1.0922" y2="-0.508" width="0.15" layer="94"/>
        <text x="0" y="-1.905" size="1.4" layer="96" rot="R180" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "GND3" : """
        <symbol name="{supply}">
        <wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.15" layer="94"/>
        <text x="0" y="-2.54" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        <wire x1="-1.27" y1="-0.635" x2="1.27" y2="-0.635" width="0.15" layer="94"/>
        <wire x1="-0.635" y1="-1.27" x2="0.635" y2="-1.27" width="0.15" layer="94"/>
        </symbol>
    """,
    "GND3:DASH" : """
        <symbol name="{supply}">
        <wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.15" layer="94" style="shortdash"/>
        <text x="0" y="-2.4892" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        <wire x1="-1.2192" y1="-0.6096" x2="1.2192" y2="-0.6096" width="0.15" layer="94" style="shortdash"/>
        <wire x1="-0.6096" y1="-1.2192" x2="0.6096" y2="-1.2192" width="0.15" layer="94" style="dashdot"/>
        </symbol>
    """,
    "GND4" : """
        <symbol name="{supply}">
        <wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.15" layer="94"/>
        <text x="0" y="-3.302" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        <wire x1="-1.27" y1="-0.635" x2="1.27" y2="-0.635" width="0.15" layer="94"/>
        <wire x1="-0.635" y1="-1.27" x2="0.635" y2="-1.27" width="0.15" layer="94"/>
        <wire x1="-0.0635" y1="-2.032" x2="0.0635" y2="-2.032" width="0.15" layer="94"/>
        </symbol>
    """,
    "ARROW2+:HALF" : """
        <symbol name="{supply}">
        <wire x1="0" y1="0" x2="-1.27" y2="-1.905" width="0.15" layer="94"/>
        <wire x1="0" y1="1.27" x2="-1.27" y2="-0.635" width="0.15" layer="94"/>
        <text x="1.778" y="-2.286" size="1.4" layer="96" rot="R90">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        <wire x1="0" y1="0" x2="0" y2="1.27" width="0.15" layer="94"/>
        </symbol>
    """,
    "ARROW2-:HALF" : """
        <symbol name="{supply}">
        <wire x1="0" y1="-2.54" x2="-1.27" y2="-0.635" width="0.15" layer="94"/>
        <wire x1="0" y1="-3.81" x2="-1.27" y2="-1.905" width="0.15" layer="94"/>
        <text x="0.508" y="-0.15" size="1.4" layer="96" rot="R270">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="0" visible="off" length="short" direction="sup" rot="R270"/>
        <wire x1="0" y1="-2.54" x2="0" y2="-3.81" width="0.15" layer="94"/>
        </symbol>
    """,
    "TRIANGLE2+" : """
        <symbol name="{supply}">
        <wire x1="0.889" y1="-1.27" x2="0" y2="0.127" width="0.15" layer="94"/>
        <wire x1="0" y1="0.127" x2="-0.889" y2="-1.27" width="0.15" layer="94"/>
        <wire x1="-0.889" y1="-1.27" x2="0.889" y2="-1.27" width="0.15" layer="94"/>
        <text x="0" y="1.778" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        <wire x1="1.397" y1="-1.27" x2="0" y2="0.889" width="0.15" layer="94"/>
        <wire x1="0" y1="0.889" x2="-1.397" y2="-1.27" width="0.15" layer="94"/>
        </symbol>
    """,
    "TRIANGLE2-" : """
        <symbol name="{supply}">
        <wire x1="-0.889" y1="1.27" x2="0" y2="-0.127" width="0.15" layer="94"/>
        <wire x1="0" y1="-0.127" x2="0.889" y2="1.27" width="0.15" layer="94"/>
        <wire x1="-0.889" y1="1.27" x2="0.889" y2="1.27" width="0.15" layer="94"/>
        <text x="0" y="-1.778" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        <wire x1="-1.397" y1="1.27" x2="0" y2="-0.889" width="0.15" layer="94"/>
        <wire x1="0" y1="-0.889" x2="1.397" y2="1.27" width="0.15" layer="94"/>
        </symbol>
    """,
    "ARROW1+" : """
        <symbol name="{supply}">
        <wire x1="1.27" y1="-1.905" x2="0" y2="0" width="0.15" layer="94"/>
        <wire x1="0" y1="0" x2="-1.27" y2="-1.905" width="0.15" layer="94"/>
        <text x="0" y="1.016" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        </symbol>
    """,
    "ARROW1-" : """
        <symbol name="{supply}">
        <wire x1="-1.27" y1="1.905" x2="0" y2="0" width="0.15" layer="94"/>
        <wire x1="0" y1="0" x2="1.27" y2="1.905" width="0.15" layer="94"/>
        <text x="0" y="-1.016" size="1.4" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "ARROW3+" : """
        <symbol name="{supply}">
        <wire x1="1.27" y1="-1.905" x2="0" y2="0" width="0.15" layer="94"/>
        <wire x1="0" y1="0" x2="-1.27" y2="-1.905" width="0.15" layer="94"/>
        <wire x1="1.27" y1="-0.635" x2="0" y2="1.27" width="0.15" layer="94"/>
        <wire x1="0" y1="1.27" x2="-1.27" y2="-0.635" width="0.15" layer="94"/>
        <text x="0" y="3.81" size="1.4" layer="96" rot="R180" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        <wire x1="0" y1="2.54" x2="-1.27" y2="0.635" width="0.15" layer="94"/>
        <wire x1="1.27" y1="0.635" x2="0" y2="2.54" width="0.15" layer="94"/>
        </symbol>
    """,
    "ARROW3-" : """
        <symbol name="{supply}">
        <wire x1="-1.27" y1="1.905" x2="0" y2="0" width="0.15" layer="94"/>
        <wire x1="0" y1="0" x2="1.27" y2="1.905" width="0.15" layer="94"/>
        <wire x1="-1.27" y1="0.635" x2="0" y2="-1.27" width="0.15" layer="94"/>
        <wire x1="0" y1="-1.27" x2="1.27" y2="0.635" width="0.15" layer="94"/>
        <text x="0" y="-3.81" size="1.4" layer="96" rot="R180" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        <wire x1="-1.27" y1="-0.635" x2="0" y2="-2.54" width="0.15" layer="94"/>
        <wire x1="0" y1="-2.54" x2="1.27" y2="-0.635" width="0.15" layer="94"/>
        </symbol>
    """,
    "ARROW3-:HALF" : """
        <symbol name="{supply}">
        <wire x1="0" y1="-2.54" x2="-1.27" y2="-0.635" width="0.15" layer="94"/>
        <wire x1="0" y1="-3.81" x2="-1.27" y2="-1.905" width="0.15" layer="94"/>
        <text x="0.508" y="-0.15" size="1.4" layer="96" rot="R270">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="0" visible="off" length="short" direction="sup" rot="R270"/>
        <wire x1="0" y1="-2.54" x2="0" y2="-3.81" width="0.15" layer="94"/>
        <wire x1="0" y1="-5.08" x2="-1.27" y2="-3.175" width="0.15" layer="94"/>
        <wire x1="0" y1="-3.81" x2="0" y2="-5.08" width="0.15" layer="94"/>
        </symbol>
    """,
    "ARROW3+:HALF" : """
        <symbol name="{supply}">
        <wire x1="0" y1="0" x2="-1.27" y2="-1.905" width="0.15" layer="94"/>
        <wire x1="0" y1="1.27" x2="-1.27" y2="-0.635" width="0.15" layer="94"/>
        <text x="1.778" y="-2.286" size="1.4" layer="96" rot="R90">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        <wire x1="0" y1="0" x2="0" y2="1.27" width="0.15" layer="94"/>
        <wire x1="0" y1="2.54" x2="-1.27" y2="0.635" width="0.15" layer="94"/>
        <wire x1="0" y1="1.27" x2="0" y2="2.54" width="0.15" layer="94"/>
        </symbol>
    """,
    "GND2:DASH" : """
        <symbol name="{supply}">
        <wire x1="-1.905" y1="0" x2="1.905" y2="0" width="0.15" layer="94"/>
        <wire x1="-1.0922" y1="-0.508" x2="1.0922" y2="-0.508" width="0.15" layer="94" style="shortdash"/>
        <text x="0" y="-1.905" size="1.4" layer="96" rot="R180" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="2.54" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "ARROW1+:HALF" : """
        <symbol name="{supply}">
        <wire x1="0" y1="0" x2="-1.27" y2="-1.905" width="0.15" layer="94"/>
        <text x="1.778" y="-2.286" size="1.4" layer="96" rot="R90">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        </symbol>
    """,
    "ARROW1-:HALF" : """
        <symbol name="{supply}">
        <wire x1="0" y1="-2.54" x2="-1.27" y2="-0.635" width="0.15" layer="94"/>
        <text x="0.508" y="-0.15" size="1.4" layer="96" rot="R270">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="0" visible="off" length="short" direction="sup" rot="R270"/>
        </symbol>
    """,
    "FLAT:UP" : """
        <symbol name="{supply}">
        <wire x1="1.905" y1="0" x2="-1.905" y2="0" width="0.15" layer="94"/>
        <text x="0" y="0.762" size="1.27" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        </symbol>
    """,
    "FLAT:DOWN" : """
        <symbol name="{supply}">
        <wire x1="1.905" y1="0" x2="-1.905" y2="0" width="0.15" layer="94"/>
        <text x="0" y="0.762" size="1.27" layer="96" align="center">&gt;VALUE</text>
        <pin name="{supply}" x="0" y="-2.54" visible="off" length="short" direction="sup" rot="R90"/>
        </symbol>
    """
}

SUPPLY_SYM_ALIAS = {
    "GND1"              : ("G", "G1", "GND", "0"),
    "GND2"              : ("G2", ),
    "GND2:DASH"         : ("G2D", "G3:D", "G2:DASH", "GND2D"),
    "GND3"              : ("G3", ),
    "GND3:DASH"         : ("G3D", "G3:D", "G3:DASH", "GND3D"),
    "GND4"              : ("G4", ),
    "COMMON"            : ("COM", ),

    "TRIANGLE+"         : ("+", "T1+", "T1"),
    "TRIANGLE-"         : ("-", "T1-"),
    "TRIANGLE2+"        : ("T2+", "T2"),
    "TRIANGLE2-"        : ("T2-", ),

    "ARROW1+"           : ("A1", "A", "A+", "A1+"),
    "ARROW1-"           : ("A1-", ),
    "ARROW1+:HALF"      : ("A1:HALF", "A1+:HALF", "A1H", "A1+H", "A1:H", "A1+:H", "ARROW1+H"),
    "ARROW1-:HALF"      : ("A1-:HALF", "A1-H", "A1-:H", "ARROW1-H"),

    "ARROW2+"           : ("A2", "A2+"),
    "ARROW2-"           : ("A2-", ),
    "ARROW2+:HALF"      : ("A2:HALF", "A2+:HALF", "A2H", "A2:H", "A2+H", "A2+:H", "ARROW2+H", "ARROW2+:H"),
    "ARROW2-:HALF"      : ("A2-:HALF", "A2-H", "A2-:H", "ARROW2-H"),

    "ARROW3+"           : ("A3", "A3+"),
    "ARROW3-"           : ("A3-", ),
    "ARROW3+:HALF"      : ("A3:HALF", "A3+:HALF", "A3H", "A3+H", "A3:H", "A3+:H", "ARROW3+H", "ARROW3+:H"),
    "ARROW3-:HALF"      : ("A3-:HALF", "A3-H", "A3-:H", "ARROW3-H"),
    "FLAT:UP"           : ("FLAT+", "F+", "FLAT"),
    "FLAT:DOWN"         : ("FLAT-", "F-"),
}

COMMAND_DOC_STYLES="""
=== Available Styles ===
{styles}
""".format(
    styles="".join(["  {:2d}) {:20s} (aliases: {})\n".format(
        idx, i, ("N/A" if (i not in SUPPLY_SYM_ALIAS) else ", ".join(SUPPLY_SYM_ALIAS[i]))
    ) for idx,i in enumerate(sorted(SUPPLY_SYM_TEMPLATES.keys()))])
)

COMMAND_DOC=COMMAND_DOC_EXAMPLES+COMMAND_DOC_STYLES+COMMAND_DOC_INFO

DEFAULT_FILE_PATH="~/EAGLE/libraries"

# Add Aliases
for k,v in SUPPLY_SYM_ALIAS.items():
    orig = SUPPLY_SYM_TEMPLATES[k]
    for i in v:
        SUPPLY_SYM_TEMPLATES[i] = orig

class L:
    DEBUG = False
    @staticmethod
    def _log (level, msg, context = None):
        prefix = f"[{level:7} {context.contextName}]" if context is not None else f"[{level:8}]"
        lines = msg.split("\n")
        for idx, i in enumerate(lines):
            if idx == len(lines)-1 and i == "":
                break
            sys.stderr.write(f"{prefix} {i}\n")
        
    @staticmethod
    def e (msg, context = None):
        L._log("Error", msg, context)
        
    @staticmethod
    def w (msg, context = None):
        L._log("Warning", msg, context)
        
    @staticmethod
    def i (msg, context = None):
        L._log("Info", msg, context)
        
    @staticmethod
    def d (msg, context = None):
        if L.DEBUG:
            L._log("Debug", msg, context)

class Util:
    @staticmethod
    def escape (esc, dbl=False):
        if dbl:
            return html.escape(html.escape(esc))
        else:
            return html.escape(esc)

    @staticmethod
    def escape2 (esc):
        return esc.replace("\"", "&quot;")

class EagleGenError(ValueError): 
    def __init__ (self, msg, *args, context = None, **kwargs):
        super().__init__(msg,*args, **kwargs)
        self.msg = msg
        self.context = context
        L.d(msg, context)
        
    def __str__ (self):
        return f"{self.__class__.__name__}: {self.msg} [Context = {context.contextName}]" if context is not None else f"{self.__class__.__name__}: {self.msg}"
    
class ValidationError(EagleGenError): pass
class FileAlreadyExists(EagleGenError): pass

class Supply:
    def __init__ (self, parent, name, style):
        self.parent = parent
        self.name = name
        self.style = style
        
        if self.style not in SUPPLY_SYM_TEMPLATES:
            raise ValidationError("Supply " + self.name + " requested symbol style " + self.symbol + " which does not exist.", context = self)
            
        L.d(f"Creating supply {self.name}.", self)
    
    @property
    def symbolData (self):
        L.d(f"Generating supply symbol using style '{self.style}'.", self)
        
        sup_name = self.name
        sup_name_quote  = Util.escape2(sup_name)
        sup_name_esc    = Util.escape(sup_name)
        sup_name_esc2   = Util.escape(sup_name, True)

        return SUPPLY_SYM_TEMPLATES[self.style].format(
            supply=sup_name_quote,
            supply_esc=sup_name_esc,
            supply_esc2=sup_name_esc2,
            supply_original=sup_name
        )
    
    @property
    def deviceData (self):
        L.d(f"Generating device.", self)
        
        sup_name        = self.name
        sup_name_quote  = Util.escape2(sup_name)
        sup_name_esc    = Util.escape(sup_name)
        sup_name_esc2   = Util.escape(sup_name, True)

        return SUPPLY_DEV_TEMPLATE.format(
            supply=sup_name_quote,
            supply_esc=sup_name_esc,
            supply_esc2=sup_name_esc2,
            supply_original=sup_name
        )
        
    @property
    def contextName (self):
        return self.parent.contextName + ":" + self.name
        
    def _clone (self, newParent):
        return Supply(newParent, self.name, self.style)
        
class Group:
    def __init__ (self, parent, name, title):
        self.parent = parent
        self.name = name
        self.title = title
        self.include = None
        self._supplies = {}
        
        L.d(f"Creating group {self.name}.", self)
        
    def createSupply (self, name, style):
        if name  in self._supplies:
            raise ValidationError("Supply " + name + " already exists.", context = self)
        self._supplies[name] = Supply(self, name, style)
        return self._supplies[name]
    
    """def importSupply (self, supply):
        if supply.name  in self._supplies:
            raise ValidationError(f"Imported supply {supply.contextName} already exists.", context = self)
        self._supplies[name] = Supply(self, name, style)
        return self._supplies[name]"""
        
    @property
    def supplies (self):
        groupsVisited = []
        return self._supplieschain(groupsVisited)
        
    @property
    def filename (self):
        return self.parent._makeFileName(self.name)
    
    def _supplieschain (self, groupVisited):
        localSupplies = self._supplies.values()
        
        if self.include is None:
            return localSupplies
        
        L.d(f"Imports {self.include.contextName} supplies.", self)
        
        if self in groupVisited:
            stack = "".join(map(groupVisited, lambda x: f"    x.name\n"))
            raise ValidationError(f"Circular inclusion of group.\nStack:\n{stack}", context = self)
            
        groupVisited.append(self)
        
        return chain(localSupplies, self.include._supplieschain(groupVisited))
            
    
    @property
    def contextName (self):
        return self.parent.contextName + ":" + self.name
    
    def validate (self):
        L.d("Validating group.", self)
        names = []
        for supply in self.supplies:
            if supply.name in names:
                raise ValidationError(f"Supply '{supply.name}' already defined in '{supply.contextName}'.", context = self)
            names.append(supply.name)
    
    def write (self):
        fn = self.filename
        
        L.d(f"Generating library '{fn}'.", self)
        
        if os.path.exists(fn):
            if not self.parent.overwrite:
                raise FileAlreadyExists(f"File '{fn}' already exists. Use --force to overwrite.", context=self)
        
        with open(fn, 'w') as fd:
            params = {}
            
            params['items'] = "".join(["&lt;li&gt;" + Util.escape(i, True) + "&lt;/li&gt;" for i in self._supplies.keys()])
            params['title'] = self.title
            params['title_esc'] = Util.escape(params['title'], True)
            
            symbols = StringIO()
            devices = StringIO()
            
            for supply in self.supplies:
                symbols.write(supply.symbolData)
                devices.write(supply.deviceData)
                
            fd.write(FILE_TEMPLATE.format(symbols=symbols.getvalue(),devices=devices.getvalue(), **params))


class Config:
    def __init__ (self, filename, basepath, prefix = ""):
        self._groups = {}
        self.filename = filename
        self.prefix = prefix
        self._basepath = basepath
        self.overwrite = False
        L.d(f"Creating configuration from {self.filename}.", self)
        
    def createGroup (self, name, title):
        if name in self._groups:
            raise ValidationError("Group " + name + " already exists.")
        self._groups[name] = Group(self, name, title)
        return self._groups[name]
        
    @property
    def groups (self):
        return self._groups.values()
        
    @property
    def contextName (self):
        return self.filename
        
    def _makeFileName (self, name):
        fn = os.path.join(self.basepath, self.prefix + name + ".lbr")
        return fn
        
    @property
    def basepath(self):
        return os.path.expanduser(self._basepath)
    
    def validate (self):
        L.d("Validating groups.", supplyConfig)
        for i in self.groups:
            i.validate()
            
    def write (self):
        L.d("Generating libraries.", self)
        for i in self.groups:
            i.write()
            
    @staticmethod
    def parse (fd, overrideOutput = None):
        fn          = fd.name
        
        L.d (f"Loading configuration from {fn}.")
        
        data        = json.load(fd)
        prefix      = data["prefix"] if "prefix" in data else ""
        out         = overrideOutput if ("output" not in data or overrideOutput is not None) else data["output"]
        
        L.d (f"Configuration loaded.")
        
        if out is None:
            out = DEFAULT_FILE_PATH
            
        config = Config(fn, out, prefix)
        
        if "groups" not in data:
            raise ValidationError("Configuration does not contain groups section.", context = config)
        
        if not type(data["groups"]) is dict:
            raise ValidationError("Configuration contains invalid group value type. Should be dictionary.", context = config)
        
        # Decode groups and supply names
        for k,v in data["groups"].items():
            if not type(v) is dict:
                raise ValidationError(f"Group {k} is not a ditionary.", context = config)
                
            title = k if "title" not in v else v["title"]
            
            group = config.createGroup(k, title)
            
            if "supplies" not in v:
                raise ValidationError("Configuration does not contain supplies section.", context = group)
                
            supplies = v["supplies"]
            
            if not isinstance(supplies, Iterable):
                raise ValidationError("Configuration contains invalid supply list. Should be list.", context = group)
                
            for supply in supplies:
                if not type(supply) is dict:
                    raise ValidationError("Configuration contains a supply that is malformed. Should be a dictionary.", context = group)
                
                if "name" not in supply:
                    raise ValidationError("Configuration contains a supply that has no name.", context = group)
                
                if "style" not in supply:
                    raise ValidationError("Configuration contains a supply without style.", context = group)
                    
                group.createSupply(supply["name"], supply["style"])
                
        # Connect group includes now that we've loaded all the groups
        for k,v in data["groups"].items():
            if "include" in v:
                include = v["include"]
                group = config._groups[k]
                
                if include not in config._groups:
                    raise ValidationError(f"Group includes signals from group '{include}' but no such group exists.", context = group)
                
                group.include = config._groups[include]
                L.d(f"Includes group '{group.include.contextName}'.", group)
                
        return config


parser = argparse.ArgumentParser(
    description='Creates an Eagle CAD supply library.',
    formatter_class=argparse.RawTextHelpFormatter,
    epilog=(COMMAND_DOC)
)

parser.add_argument(
    'config',
    type=argparse.FileType('r'),
    help="A JSON file containing a description of the supplies."
)

parser.add_argument(
    '--out',
    help=f"Path to output directory. May be specified in json. If not specified in either, defaults to '{DEFAULT_FILE_PATH}'.",
    required=False
)

parser.add_argument(
    '--debug',
    action='store_true',
    help="Enable debug logs."
)

parser.add_argument(
    '--force',
    action='store_true',
    help="Overwrite files if they already exist."
)

parser.add_argument(
    '--mkdir',
    action='store_true',
    help="Create directory if needed."
)

args = parser.parse_args()

if args.debug:
    L.DEBUG=True

try:
    supplyConfig = Config.parse(args.config, args.out)
    
    if args.force:
        supplyConfig.overwrite = True
        
    L.i(f"Validating...")
    supplyConfig.validate()
    
    if os.path.exists(supplyConfig.basepath):
        if not os.path.isdir(supplyConfig.basepath):
            raise ValidationError(f"Path '{supplyConfig.basepath}' must be a directory.", context = supplyConfig)
    else:
        if args.mkdir:
            os.makedirs(supplyConfig.basepath)
        else:
            raise ValidationError(f"Path '{supplyConfig.basepath}' doesn't exist.", context = supplyConfig)
            
    L.i(f"Generating...")
    supplyConfig.write()
    
    if len(supplyConfig.groups) > 0:
        L.i(f"Successfully generated libraries:")
        for i in supplyConfig.groups:
            L.i(f"   {i.filename}")
    
    L.i(f"Successfully generated supplies.")
except Exception as e:
    if isinstance(e, json.JSONDecodeError):
        L.e(f"Unable to load configuration due to a JSON parsing error.")
        L.e(f"Cause:        {e.msg}")
        L.e(f"Location:     {e.lineno}:{e.colno}")
        L.e(f"File:         {args.config.name}")
        
        L.d(f"--Full Exception--", e.context)
        L.d("".join(traceback.format_exception(None, e, e.__traceback__)), e.context)
    elif isinstance(e, EagleGenError):
        L.e(f"Error processing configuration.", e.context)
        L.e(f"Cause:        {e.msg}", e.context)
        
        L.d(f"--Full Exception--", e.context)
        L.d("".join(traceback.format_exception(None, e, e.__traceback__)), e.context)
    elif isinstance(e, OSError):
        L.e(f"I/O Error. ({errno})")
        L.e(f"Cause:        {e.strerror}")
        L.e(f"File:         {e.filename}")
        
        L.d(f"--Full Exception--", e.context)
        L.d("".join(traceback.format_exception(None, e, e.__traceback__)), e.context)
    else:
        L.e(f"An exception occurred:")
        L.e("".join(traceback.format_exception(None, e, e.__traceback__)))

