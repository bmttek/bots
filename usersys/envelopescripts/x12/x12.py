import os, sys
import bots.botsglobal as botsglobal
import bots.botslib as botslib
from datetime import datetime

def ta_infocontent(ta_info,*args,**kwargs):
    ta_info["ISA05"]="ZZ"
    ta_info["ISA07"]="ZZ"
    #ta_info["GS06"]=ta_info["alt"]
    #ta_info["ISA13"]=ta_info["alt"]
    ta_info["version"]="00306"
    now = datetime.now()
    dt = now.strftime('%y%m%d')
    ta_info["GS04"]=dt

def envelopecontent(ta_info,out,*args,**kwargs):
    now = datetime.now()
    dt = now.strftime('%y%m%d')
    out.change(where=({'BOTSID':'ISA'},{'BOTSID':'GS'},),change={'GS04': dt})
