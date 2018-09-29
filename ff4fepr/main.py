from core import BinaryList, toint
from output import error, warning, optional_output
from datetime import datetime
import random
import magemods
import learned_spells
import starting_stats
import starting_equip
import battlemenus
import weapons
import drops
import monsters
import shops
import spelldata
from starting_spells import groupspells
from pprint import pprint as pp

def render_opfilename(infname, seed):
    if infname.endswith('.smc'):
        return '%s-pr%s.smc' % (infname[:-4], seed)

def main(args):
    debug, verbose = optional_output(args)
    default_seed=str((datetime.today() - datetime.fromordinal(1)).seconds)
    seed = args.seed if args.seed is not None else default_seed
    random.seed(seed)
    if args.output is None:
        output_fname = render_opfilename(args.rompath, seed)
    else:
        output_fname=args.output
    romdata=BinaryList(args.rompath,
                       output_fname=output_fname,
                       verbose=verbose,
                       debug=debug)
    if args.rydia_allrares:
        magemods.rydiacalls(romdata, "Imp*,Bomb*,Cockatrice*,Mage*")
        spelldata.birdcall(romdata)
    if args.rydia_starting_calls is not None:
        magemods.rydiacalls(romdata, args.rydia_starting_calls)
    if args.rydia_random_calls is not None:
        magemods.rydiacalls_random(romdata, args.rydia_random_calls)
    if args.uber_tellah:
        magemods.addspellset(romdata, 'uber-tellah')
    if args.paladin_spells:
        magemods.replacelearnedsets(romdata, 'paladin-magic')
    if args.dump_learned:
        for lsp in learned_spells.loadlearnedspells(romdata).items():
            print lsp
    if args.dump_starting_spells:
        for itm in groupspells(romdata):
            print itm
    if args.set_char_stats:
        starting_stats.setcharstats(romdata, args.set_char_stats)
    if args.dump_starting_stats:
        starting_stats.dumpstartingstats(romdata)
    if args.dump_menus:
        battlemenus.dump2screen(romdata)
    if args.dump_equip:
        starting_equip.dump2screen(romdata)
    if args.dual_wield is not None:
        starting_stats.setdualwields(romdata, args.dual_wield)
    if args.add_spells_to_weapons is not None:
        weapons.addspells2weapons_arg(romdata, args.add_spells_to_weapons)
    if args.replace_commandset is not None:
        battlemenus.replace_commandset_args(romdata,
                                            args.replace_commandset)
    if args.uptco_edward:
        starting_equip.uptco_edward(romdata)
        starting_stats.uptco_edward(romdata)
        battlemenus.uptco_edward(romdata)
    if args.dump_weapons:
        weapons.dump2screen(romdata)
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
            variance=map(toint, tokens[0].split(','))
            changeset=tokens[1]
        changes2dump = weapons.vary_weaponstat(romdata, 'attack', variance, categories=changeset.split(','))
        for wname, oldval, newval in changes2dump:
            verbose("%s: %s->%s\n" % (wname, oldval, newval))
    if args.modup_weaponatk:
        changes2dump=weapons.modup_weaponatk(romdata)
        for wname, oldval, newval in changes2dump:
            verbose("%s: %s->%s\n" % (wname, oldval, newval))
    if args.restore_j_drops:
        drops.setjdroptables(romdata)
    if args.test_weapons:
        weapons.weapon2rom(romdata, weapons.loadweapons(romdata))
    if args.test_drops:
        drops.testdroptables(romdata)
    if args.dump_drops:
        drops.dump2screen(romdata)
    if args.randomize_drops:
        drops.randomize_all
    if args.dump_monsters:
        monsters.dumpsplits(romdata, jadjust=args.jv)
    if args.test_monsters:
        monsters.test_monsters(romdata, jadjust=args.jv)
    if args.dump_monster_itemtables:
        monsters.dumpitemtables(romdata, jadjust=args.jv)
    if args.dump_monster_drops:
        monsters.dumpmonsterdrops(romdata, jadjust=args.jv)
    if args.dump_spells:
        spelldata.dumpspellstats(romdata)
    if args.test_spells:
        spelldata.testspelldata(romdata)
    if args.bird:
        spelldata.birdcall(romdata)
    if args.test_encoding is not None:
        spelldata.testencode(args.test_encoding)
    if args.remove_bossbit is not None or args.add_bossbit is not None:
        addbossbit=args.add_bossbit.split(',') if args.add_bossbit is not None else []
        removebossbit=args.remove_bossbit.split(',') if args.remove_bossbit is not None else []
        spelldata.changebossbit(romdata,
                                hasbossbit=addbossbit,
                                nobossbit=removebossbit)
    if args.apply:
        romdata.swrite()
    else:
        romdata.showmods()
