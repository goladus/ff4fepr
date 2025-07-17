import sys
from .core import BinaryList, toint
from .output import error, warning, optional_output
from datetime import datetime
import random
from . import magemods
from . import learned_spells
from . import starting_stats
from . import starting_equip
from . import battlemenus
from . import weapons
from . import drops
from . import monsters
from . import shops
from . import spelldata
from . import ff4text
from . import equip
from . import webform
from . import scriptgen
from . import leveldata
from . import monstermods
from . import chests
from . import allitems
from .starting_spells import groupspells
from pprint import pprint as pp

def render_opfilename(infname, seed):
    if infname.endswith('.smc'):
        return '%s-pr%s.smc' % (infname[:-4], seed)

def hexjoin(numlst):
    return ','.join([hex(x) for x in numlst])

def main(args):
    """string_of_args and string_of_flags are only used
    for generating html form when that option is enabled."""
    debug, verbose = optional_output(args)
    default_seed=str((datetime.today() - datetime.fromordinal(1)).seconds)
    seed = args.seed if args.seed is not None else default_seed
    random.seed(seed)
    if args.rompath is not None:
        if args.output is None:
            output_fname = render_opfilename(args.rompath, seed)
        else:
            output_fname=args.output
        romdata=BinaryList(args.rompath,
                           output_fname=output_fname,
                           verbose=verbose,
                           debug=debug)
    else:
        romdata=None
    debug("romdata: %s\n" % type(romdata))
    if args.rydia_allrares:
        magemods.rydiacalls(romdata, "Imp*,Bomb*,Cockatrice*,Mage*")
        spelldata.birdcall(romdata)
    if args.rydia_starting_calls is not None:
        magemods.rydiacalls(romdata, args.rydia_starting_calls)
    if args.rydia_random_calls is not None:
        magemods.rydiacalls_random(romdata, args.rydia_random_calls)
    if args.uber_tellah:
        magemods.addspellset(romdata, 'uber-tellah')
    if args.medusa:
        weapons.medusa2x(romdata)
    if args.edtest:
        weapons.edweaponbuff(romdata)
        weapons.edspoon(romdata)
        weapons.staffcheat(romdata)
    if args.spoonjoke:
        weapons.spoonjoke(romdata)
    if args.paladin_spells:
        magemods.replacelearnedsets(romdata, 'paladin-magic')
    if args.set_cast_times:
        spelldata.setcasttimes(romdata, args.set_cast_times)
    if args.ct_rebalance:
        spelldata.ctrebalance(romdata)
    if args.xp_imp is not None:
        monstermods.xpimps(romdata, toint(args.xp_imp))
    if args.yang_post60hp:
        leveldata.yangpost60hp(romdata)
    if args.any_weapon:
        weapons.anyweapon(romdata)
    if args.coral_sword:
        weapons.ancient2coral(romdata)
    if args.randomize_spell_progression is not None:
        level_modifier=toint(args.randomize_spell_progression)
        magemods.randomize_learned_spells2(romdata,
                                           level_modifier=level_modifier)
    if args.randomize_spell_progression_3 is not None:
        dr=args.randomize_spell_progression_3
        magemods.randomize_learned_spells3(romdata,
                                           difficulty_ratio=dr)
    if args.randomize_learned is not None:
        spellsets=args.randomize_learned.split(',')
        magemods.randomize_learned_spells1(romdata, spellsets)
    if args.dump_learned:
        learned_spells.dump2screen(romdata)
    if args.dump_starting_spells:
        for itm in groupspells(romdata):
            print(itm)
    if args.set_char_stats:
        starting_stats.setcharstats(romdata, args.set_char_stats)
    if args.dump_starting_stats:
        starting_stats.dumpstartingstats(romdata)
    if args.dump_menus:
        battlemenus.dump2screen(romdata)
    if args.dump_monster_names:
        monsters.dumpnames(romdata)
    if args.dump_weapon_by is not None:
        weapons.dumpby(romdata, args.dump_weapon_by)
    if args.dump_weapon_racial:
        weapons.dumpracial(romdata)
    if args.dump_equip:
        starting_equip.dump2screen(romdata)
    if args.dump_eqtables:
        equip.dumpindexes(romdata)
    if args.dual_wield is not None:
        starting_stats.setdualwields(romdata, args.dual_wield)
    if args.add_spells_to_weapons is not None:
        weapons.addspells2weapons_arg(romdata, args.add_spells_to_weapons)
    if args.replace_commandset is not None:
        battlemenus.replace_commandset_args(romdata,
                                            args.replace_commandset)
    if args.special:
        starting_equip.uptco_edward(romdata)
        starting_stats.uptco_edward(romdata)
        battlemenus.uptco_edward(romdata)
    if args.dump_weapons:
        weapons.dump2screen(romdata)
    if args.dump_chests:
        chests.dumpchests(romdata)
    if args.dump_chests2:
        chests.dumpchests2(romdata)
    if args.dump_vanichests:
        chests.dump_vanichests(romdata)
    if args.vanilla_chest_search:
        chests.vanilla_search(romdata)
    if args.search_chests:
        chests.chestsearch(romdata)
    if args.dump_menu_text:
        battlemenus.dump_menu_text(romdata)
    if args.dump_itemnames:
        weapons.dumpnames(romdata)
    if args.dump_spell is not None:
        spelldata.dumpspell(romdata, args.dump_spell)
    if args.fix_dummies:
        allitems.fix_dummies(romdata)
        battlemenus.fix_dummy_menus(romdata)
    if args.dump_itemkeys:
        for itm in weapons.items:
            sys.stdout.write("%s\n" % itm)
    if args.dump_spellkeys:
        for itm in weapons.spells:
            sys.stdout.write("%s\n" % itm)
    if args.modify_offset is not None:
        offset_string, value_string = args.modify_offset.split('=')
        offset_to_change = toint(offset_string)
        value = toint(value_string)
        romdata.addmod(offset_to_change, value)
    if args.hitratings:
        weapons.hitrating(romdata)
    if args.tpassbuff:
        shops.tpassbuff(romdata)
    if args.shuffle_weaponatk is not None:
        changesets=args.shuffle_weaponatk.split(':')
        changes2dump=[]
        for changeset in changesets:
            changes2dump += weapons.shuffle_weaponstat(romdata, 'attack', changeset.split(','))
        for wname, oldval, newval in changes2dump:
            verbose("%s: %s->%s\n" % (wname, oldval, newval))
    if args.vary_weaponatk is not None:
        tokens=args.vary_weaponatk.split(':')
        if len(tokens) == 1:
            changeset=tokens[0]
            variance=(-5, 15)
        else:
            variance=list(map(toint, tokens[0].split(',')))
            changeset=tokens[1]
        changes2dump = weapons.vary_weaponstat(romdata, 'attack', variance, categories=changeset.split(','))
        for wname, oldval, newval in changes2dump:
            verbose("%s: %s->%s\n" % (wname, oldval, newval))
    if args.modup_weaponatk:
        changes2dump=weapons.modup_weaponatk(romdata)
        for wname, oldval, newval in changes2dump:
            verbose("%s: %s->%s\n" % (wname, oldval, newval))
    if args.modify_shop is not None:
        shops.modify_shop(romdata, args.modify_shop)
    if args.restore_j_drops:
        drops.setjdroptables(romdata)
    if args.dk_equip:
        equip.darkknight_equip(romdata)
    if args.edit_vchest is not None:
        chests.vanichest_edit(romdata, args.edit_vchest)
    if args.test_levelup:
        leveldata.testludata(romdata)
    if args.test_eqtables:
        equip.testeq(romdata)
    if args.test_weapons:
        weapons.weapon2rom(romdata, weapons.loadweapons(romdata))
    if args.test_drops:
        drops.testdroptables(romdata)
    if args.test_shops:
        shops.testshops(romdata)
    if args.test_menus:
        battlemenus.testcommands(romdata)
    if args.modify_menu is not None:
        battlemenus.modify_menu(romdata, args.modify_menu)
    if args.replace_menu is not None:
        battlemenus.replace_menu(romdata, args.replace_menu)
    if args.dump_shops:
        shops.dumpshops(romdata)
    if args.dump_drops:
        drops.dump2screen(romdata)
    if args.randomize_drops:
        drops.randomize_all(romdata)
    if args.buff_starting_equip is not None:
        starting_equip.setall_eqlevel(romdata, args.buff_starting_equip)
    if args.dump_monsters:
        try:
            monsters.dumpsplits(romdata, jadjust=args.jv)
        except BrokenPipeError:
            sys.exit(32)
    if args.dump_monsters_raw:
        monsters.dumpmondict(romdata, jadjust=args.jv)
    if args.dump_monsters_csv:
        monsters.dump2csv(romdata, jadjust=args.jv)
    if args.dump_monsters_and_bosses_csv:
        monsters.dump2csv(romdata, bosses=True, jadjust=args.jv)
    if args.dump_monster_values is not None:
        monsters.dumpkeys(romdata, args.dump_monster_values.split(','))
    if args.test_monsters:
        monsters.test_monsters(romdata, jadjust=args.jv)
    if args.dump_monster_itemtables:
        monsters.dumpitemtables(romdata, jadjust=args.jv)
    if args.dump_monster_drops:
        monsters.dumpmonsterdrops(romdata, jadjust=args.jv)
    if args.dump_spells:
        spelldata.dumpspellstats(romdata)
    if args.dump_levelup:
        leveldata.dump2screen(romdata)
    if args.test_spells:
        spelldata.testspelldata(romdata)
    if args.modify_monster is not None:
        monsters.modify_monster(romdata, args.modify_monster, jadjust=args.jv)
    if args.bird:
        spelldata.birdcall(romdata)
    if args.test_encoding is not None:
        ff4text.testencode(args.test_encoding)
    if args.encode is not None:
        ff4text.encode(args.encode)
    if args.decode is not None:
        ff4text.decode(args.decode)
    if args.remove_bossbit is not None or args.add_bossbit is not None:
        addbossbit=args.add_bossbit.split(',') if args.add_bossbit is not None else []
        removebossbit=args.remove_bossbit.split(',') if args.remove_bossbit is not None else []
        spelldata.changebossbit(romdata,
                                hasbossbit=addbossbit,
                                nobossbit=removebossbit)
    if args.generate_form:
        webform.genform1(args)
    if args.dump_generator:
        scriptgen.dumpall(romdata, args)
    if args.find_bytes is not None:
        bytes2find = [toint(x) if x != 'X' else None for x in args.find_bytes.split(',')]
        for xoffset in romdata.find2(bytes2find):
            print(xoffset, hex(xoffset), hexjoin(romdata[xoffset:xoffset+len(bytes2find)]))
            #print(xoffset, hex(xoffset), romdata[xoffset:xoffset+len(bytes2find)])
    if args.find_bytes10 is not None:
        bytes2find = [toint(x) for x in args.find_bytes10.split(',')]
        for xoffset in romdata.find(bytes2find):
            before = romdata[xoffset-10:xoffset]
            after = romdata[xoffset+1:xoffset+10]
            outputstr = '%s|%s|%s' % (','.join([hex(x) for x in before]), romdata[xoffset], ','.join([hex(x) for x in after]))
            print(xoffset, hex(xoffset), outputstr)
    if args.dump_offsets is not None:
        _startoff, _nbytes = (args.dump_offsets.split('+') + [1])[:2]
        startoff = toint(_startoff)
        nbytes = toint(_nbytes)
        print(','.join([hex(x) for x in romdata[startoff:startoff+nbytes]]))
    if args.apply:
        romdata.swrite()
    else:
        if romdata is not None:
            romdata.showmods()
