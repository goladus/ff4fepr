from ff4data import *
from monsters import splitmonsters, monsearch, mondict2rom

def xpimps(romdata, newvalue):
    mondata=splitmonsters(romdata)
    monsters=monsearch(mondata, 'name', 'Imp')
    mondata[monsters[0]]['xp']=newvalue
    mondict2rom(romdata, mondata)
