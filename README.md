## FFIV Free Enterprise Post-Randomizer

This tool is designed to make additional modifications and randomizations to a seed generated by [Final Fantasy IV - Free Enterprise](http://ff4fe.com), a fantastic "open world randomizer" romhack for Final Fantasy IV, by B0ardface.

### Warning about Cheating

Please note that this tool is (currently) intended only for casual and experimental use.  Use of this tool on a race rom before or during a league race or any other official FF4FE race on SpeedRunsLive is considered cheating and will result in disqualification and a ban from SRL.

### Why a Post-Randomizer?

Final Fantasy IV Free Enterprise is a truly excellent romhack, and is notable as much for what it doesn't do as what it does.  FF4FE has a distinct vision and mission.  It is an open world hack designed for speedrunning and racing.  While fixing bugs and making occasional tweaks here and there, ff4fe is very disciplined and deliberately preserves vanilla behavior whenever possible.  The original FF4 has a great deal of depth and Free Enterprise really enables that depth to shine through while keeping the hack familiar and accessible to players who loved the original game.  FF4FE is also highly polished, with many of great and subtle quality-of-life features.

All that said, some players are interested in more reckless or crazy modifications that aren't appropriate for FF4FE's disciplined approach.  These ideas may include rebalancing weaker characters like Edward and Dark Knight Cecil, or difficulty hacks such as randomizing the cast times on all spells.  Other ideas may just be a lower priority.

Using hacks on the vanilla game is one option, but speaking personally I really love the Free Enterprise hack and at this point would rather play it than the original in most cases.

### Using ff4fepr

Currently, this tool has no official distribution mechanism.  It's developed for Python 2.7 and has been tested on [Cygwin](http://www.cygwin.com) (but uses minimal libraries so probably works in any POSIX environment).

```
usage: ff4fe-post-randomizer [-h] [--seed SEED] [--output OUTPUT]
                             [--shuffle-weaponatk SHUFFLE_WEAPONATK]
                             [--vary-weaponatk VARY_WEAPONATK]
                             [--rydia-random-calls RYDIA_RANDOM_CALLS]
                             [--rydia-starting-calls RYDIA_STARTING_CALLS]
                             [--replace-commandset REPLACE_COMMANDSET]
                             [--dual-wield DUAL_WIELD]
                             [--add-bossbit ADD_BOSSBIT]
                             [--remove-bossbit REMOVE_BOSSBIT] [--apply]
                             [--version] [--verbose] [--debug] [--jv]
                             [--randomize-drops] [--modup-weaponatk]
                             [--uber-tellah] [--paladin-spells]
                             [--set-j-drops] [--dump-learned]
                             [--dump-starting-spells] [--dump-starting-stats]
                             [--dump-menus] [--dump-equip] [--dump-weapons]
                             [--dump-drops] [--dump-monsters]
                             [--dump-monster-itemtables]
                             [--dump-monster-drops] [--dump-spells]
                             [--hitratings] [--test-monsters] [--test-weapons]
                             [--test-drops] [--test-spells] [--tpassbuff]
                             [--uptco-edward]
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
  --shuffle-weaponatk SHUFFLE_WEAPONATK
                        Shuffles weapon attack power within specified weapon categories.
  --vary-weaponatk VARY_WEAPONATK
                        Varies weapon attack power by -5 to 15.
  --rydia-random-calls RYDIA_RANDOM_CALLS
                        Rydia starts with additional call spells.  Arg: <1 to 4 spells to add>
  --rydia-starting-calls RYDIA_STARTING_CALLS
                        Add additional spells to Rydia's starting calls.  Arg: spells to add.
  --replace-commandset REPLACE_COMMANDSET
                        Replaces the commandset for specified character.  Arg: <CharnameJoin>=<cmd1>,<cmd2>,<cmd3>
  --dual-wield DUAL_WIELD
                        Sets the character's handedness to R+L.  Arg: <Charname>
  --add-bossbit ADD_BOSSBIT
                        Add boss bit to comma-delimited list of spells
  --remove-bossbit REMOVE_BOSSBIT
                        Removes boss bit from comma-delimited list of spells
  --apply, -a
  --version, -V
  --verbose, -v
  --debug, -d
  --jv, -j
  --randomize-drops     Randomizes all drop tables.
  --modup-weaponatk     Runs a preprogrammed set of various randomizations on weapon attack.
  --uber-tellah         Tellah starts with some overpowered enemy abilities
  --paladin-spells      Add some higher-level white spells to Cecil's Paladin magic
  --set-j-drops         Restore the monster drop tables from FF4j
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
  --hitratings          list attack * hitrate for each weapon
  --test-monsters       Test loading monsters and dumping to rom with no changes
  --test-weapons        Test loading weapons into memory and dumping to rom with no changes.
  --test-drops          Test loading drop tables and dumping to rom with no changes.
  --test-spells         Test loading and writing spell stats with no changes.
  --tpassbuff           Add Bacchus, Silkweb, StarVeil, Elixir, and Spoon to Troia Pass Shop
```
