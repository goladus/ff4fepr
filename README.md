## FFIV Free Enterprise Post-Randomizer

This tool is designed to make additional modifications and randomizations to a seed generated by [Final Fantasy IV - Free Enterprise](http://ff4fe.com), a fantastic "open world randomizer" romhack for Final Fantasy IV, by B0ardface.

### Current Status

Ff4fepr is currently focused on implementing python libraries for extracting data from and modifing the Final Fantasy IV/Free Enterprise ROM.  Although much of this is replicating PinkPuff's work on ff4kster, that tool is designed as a manual editor.  This is intended to be a programmatic one, with feature more suitable to making a variety of large-scale changes based on rules and logic, which is what most randomizers do.  The included command-line tool is primarily developed for testing libraries, though it is still usable to make modifications and randomizations to Free Enterprise rom files.

The API, such as it is, is still entirely in flux, largely undocumented and subject to change.

### Warning about Cheating

Please note that this tool is (currently) intended only for casual and experimental use.  Use of this tool on an Free Enterprise race rom before or during a league race or any other official FF4FE race on SpeedRunsLive is considered cheating and will result in disqualification and a ban from SRL.

### Why a Post-Randomizer?

Final Fantasy IV Free Enterprise is a truly excellent romhack, and is notable as much for what it doesn't do as what it does.  FF4FE has a distinct vision and mission.  It is an open world hack designed for speedrunning and racing.  While fixing bugs and making occasional tweaks here and there, ff4fe is very disciplined and deliberately preserves vanilla behavior whenever possible.  The original FF4 has a great deal of depth and Free Enterprise really enables that depth to shine through while keeping the hack familiar and accessible to players who loved the original game.  FF4FE is also highly polished, with many of great and subtle quality-of-life features.

All that said, some players are interested in more reckless or crazy modifications that aren't appropriate for FF4FE's disciplined approach.  These ideas may include rebalancing weaker characters like Edward and Dark Knight Cecil, or difficulty hacks such as randomizing the cast times on all spells.  Other ideas may just be a lower priority.  My hope is that this tool can at least somewhat address this desire, even if it's ultimately only in a casual fashion.

### Using ff4fepr

Currently, this tool has no official distribution mechanism.  It's developed for Python 2.7 and has been tested on [Cygwin](http://www.cygwin.com) (but uses minimal libraries so probably works in any POSIX environment).  To use this on windows without Cygwin, you'll need to set up a batch file or powershell script that passes `ff4fe-post-randomizer` to `python.exe`.  It will look something like this:

```
.\Scripts\python.exe .\Scripts\ff4fe-post-randomizer %*
```

`ff4fe-post-randomizer -h`
```

usage: ff4fe-post-randomizer [-h] [--seed SEED] [--output OUTPUT]
                             [--add-spells-to-weapons ADD_SPELLS_TO_WEAPONS]
                             [--shuffle-weaponatk SHUFFLE_WEAPONATK]
                             [--vary-weaponatk VARY_WEAPONATK]
                             [--rydia-random-calls RYDIA_RANDOM_CALLS]
                             [--rydia-starting-calls RYDIA_STARTING_CALLS]
                             [--replace-commandset REPLACE_COMMANDSET]
                             [--dual-wield DUAL_WIELD]
                             [--set-char-stats SET_CHAR_STATS]
                             [--set-cast-times SET_CAST_TIMES]
                             [--add-bossbit ADD_BOSSBIT]
                             [--remove-bossbit REMOVE_BOSSBIT]
                             [--test-encoding TEST_ENCODING] [--apply]
                             [--version] [--verbose] [--debug] [--jv]
                             [--rydia-allrares] [--dk-equip]
                             [--randomize-drops] [--modup-weaponatk]
                             [--uber-tellah] [--paladin-spells]
                             [--restore-j-drops] [--bird] [--ct-rebalance]
                             [--coral-sword] [--any-weapon] [--dump-learned]
                             [--dump-starting-spells] [--dump-starting-stats]
                             [--dump-menus] [--dump-equip] [--dump-weapons]
                             [--dump-drops] [--dump-monsters]
                             [--dump-monster-itemtables]
                             [--dump-monster-drops] [--dump-spells]
                             [--dump-eqtables] [--dump-itemnames]
                             [--dump-itemkeys] [--dump-spellkeys]
                             [--generate-form] [--hitratings]
                             [--test-monsters] [--test-weapons] [--test-drops]
                             [--test-spells] [--test-eqtables] [--tpassbuff]
                             [--special]
                             [rompath]

Final Fantasy 4 Free Enterprise Post-Randomizer

This tool dumps information or makes modifications to a specified smc file.
Currently, the smc file must be a raw, uncompressed file.
By default, no modifications are written to disk.  The --apply/-a flag
will write a new file to disk.  The new file will be in the same location
as the original rom, with the seed appended to the original filename.

positional arguments:
  rompath

optional arguments:
  -h, --help            show this help message and exit
  --seed SEED, -s SEED  specify a seed for random functions
  --output OUTPUT, -o OUTPUT
                        specify an output file
  --add-spells-to-weapons ADD_SPELLS_TO_WEAPONS
                        Add spell to weapon Arg: WeaponName=Spell:Visual:Power,Weapon2=Spell:Visual:Power
  --shuffle-weaponatk SHUFFLE_WEAPONATK
                        Shuffles weapon attack power within specified weapon categories.
  --vary-weaponatk VARY_WEAPONATK
                        Varies weapon attack power by -5 to 15.
  --rydia-random-calls RYDIA_RANDOM_CALLS
                        Rydia starts with additional call spells.  Arg: <1 to 4 spells to add>
  --rydia-starting-calls RYDIA_STARTING_CALLS
                        Add additional spells to Rydia's starting calls.  Arg: spells to add.
  --replace-commandset REPLACE_COMMANDSET
                        Replaces the commandset for specified character.  Arg: <CharnameJoin>:<cmd1>,<cmd2>,<cmd3>
  --dual-wield DUAL_WIELD
                        Sets the character's handedness to R+L.  Arg: <Charname>
  --set-char-stats SET_CHAR_STATS
                        Sets starting stats for characters.  Example: KidRydia:hp=300,maxhp=300,maxmp=50.Rosa:agi=20
  --set-cast-times SET_CAST_TIMES
                        Sets cast time for spells.  "Meteo*=5,Quake*=8"
  --add-bossbit ADD_BOSSBIT
                        Add boss bit to comma-delimited list of spells
  --remove-bossbit REMOVE_BOSSBIT
                        Removes boss bit from comma-delimited list of spells
  --test-encoding TEST_ENCODING
                        Prints the ff4 hex codes for provided string
  --apply, -a
  --version, -V
  --verbose, -v
  --debug, -d
  --jv, -j
  --rydia-allrares      Rydia starts with all four rare call spells (also renames the Dummied cockatrice spell)
  --dk-equip            Dark Knight Cecil gains access to most equipment shared by Kain and Paladin Cecil
  --randomize-drops     Randomizes all drop tables.
  --modup-weaponatk     Runs a preprogrammed set of various randomizations on weapon attack.
  --uber-tellah         Tellah starts with some overpowered enemy abilities
  --paladin-spells      Add some higher-level white spells to Cecil's Paladin magic
  --restore-j-drops     Restore the monster drop tables from FF4j
  --bird                Rename Dummied Cockatrice spell to Bird
  --ct-rebalance        Reduce cast delay on some Black and Summon magic (elementals and Meteo)
  --coral-sword         Replaces the Ancient Sword with a Lightning-elemental Coral Sword.
  --any-weapon          Allows any character/class to use any weapon.
  --dump-learned        Dump spell progressions from rom to screen.
  --dump-starting-spells
                        Dump starting spells from rom to screen.
  --dump-starting-stats
                        Dump starting stats from rom to screen.
  --dump-menus          Dump character battle menus from rom to screen.
  --dump-equip          Dump character starting equipment from rom to screen.
  --dump-weapons        Dump weapon data from rom to screen.
  --dump-drops          Dump enemy stea/drop data from rom to screen.
  --dump-monsters       Dump monster data to screen.
  --dump-monster-itemtables
                        Dump monster item table numbers and drop rates to screen.
  --dump-monster-drops  Dump monster drop data to screen. (resolves item-table)
  --dump-spells         Dump spell stats
  --dump-eqtables       Dump class equip tables
  --dump-itemnames      Dump item names from rom.
  --dump-itemkeys       Dump item names used by ff4fepr
  --dump-spellkeys      Dump spell names used by ff4feper
  --generate-form       Generate web form from script options (doesn't do much atm)
  --hitratings          list attack * hitrate for each weapon
  --test-monsters       Test loading monsters and dumping to rom with no changes
  --test-weapons        Test loading weapons into memory and dumping to rom with no changes.
  --test-drops          Test loading drop tables and dumping to rom with no changes.
  --test-spells         Test loading and writing spell stats with no changes.
  --test-eqtables       Test loading and writing equip tables with no changes.
  --tpassbuff           Add Bacchus, Silkweb, StarVeil, Elixir, and Spoon to Troia Pass Shop
  --special             ????
```
