# scan
mame scanner in python

1. create the main config pointing to your roms
2. create a config for a system
3. pass that system to `scan.py`

config example

```
name: 32x
display_name: Sega 32x
format: mamesl
mode: file
exec: mame
ini: ~/.mame/mame.ini
rom_dir: MAME_BASE_DIR_SOFT_ROMS/SYSTEM_NAME
art_dir: MAME_BASE_DIR_SOFT_ART/SYSTEM_NAME
data_dir: MAME_BASE_DIR/hash
working_dir: system-working-dir
extensions: zip
mister_core: 32x
extension: zip
cmd: GAME_EXEC SYSTEM_NAME -cart ROM_NAME
```

json output
```
./scan.py --system 32x --output-mode json

{
  "system": {
    "name": "32x",
    "display_name": "Sega 32x",
    "format": "mamesl",
    "mode": "file",
    "exec": "mame",
    "ini": "~/.mame/mame.ini",
    "rom_dir": "/mnt/roms/MAME/MAME - Software List ROMs/32x",
    "art_dir": "/mnt/roms/4emus/artwork/mamesl/32x",
    "data_dir": "MAME_BASE_DIR/hash",
    "working_dir": "system-working-dir",
    "extensions": "zip",
    "mister_core": "32x",
    "extension": "zip",
    "cmd": "mame 32x -cart ROM_NAME"
  },
  "entries": {
    "doom": {
      "name": "Doom (Europe)",
      "description": "Doom (Europe)",
      "name_rom": "doom",
      "name_pretty": "Doom (Europe) (doom)",
      "name_sl": "",
      "rom_abspath": "/mnt/roms/MAME/MAME - Software List ROMs/32x/doom.zip",
      "year": "1994",
      "manufacturer": "Sega",
      "driver_status": "good",
      "display_orientation": 0,
      "players": 0
    },
  }
}
```

yaml output
```
./scan.py --system 32x --output-mode yaml

system:
  name: 32x
  display_name: Sega 32x
  format: mamesl
  mode: file
  exec: mame
  ini: ~/.mame/mame.ini
  rom_dir: /mnt/roms/MAME/MAME - Software List ROMs/32x
  art_dir: /mnt/roms/4emus/artwork/mamesl/32x
  data_dir: MAME_BASE_DIR/hash
  working_dir: system-working-dir
  extensions: zip
  mister_core: 32x
  extension: zip
  cmd: mame 32x -cart ROM_NAME
entries:
  doom:
    name: Doom (Europe)
    description: Doom (Europe)
    name_rom: doom
    name_pretty: Doom (Europe) (doom)
    name_sl: ''
    rom_abspath: /mnt/roms/MAME/MAME - Software List ROMs/32x/doom.zip
    year: '1994'
    manufacturer: Sega
    driver_status: good
    display_orientation: 0
    players: 0
```

pegasus output
```
./scan.py --system 32x --output-mode pegasus

collection: Sega 32x
extension: zip
launch: mame 32x -cart {file.name}

game: Doom (Europe)
file: /mnt/roms/MAME/MAME - Software List ROMs/32x/doom.zip
developer: Sega
year: 1994
genre: Unspecified
players: 0
description: Doom (Europe)
rating: Unspecified


```

mister output
```
./scan.py --system 32x --output-mode mister

MisterFPGA support started
 Time taken: 0.005811s
Reading items from /mnt/roms/MAME/MAME - Software List ROMs/32x
 Found 44 items
Total titles found: 44
Received data from mame
 Time taken: 0.004615s
Summary
 Time taken: 0.076086s
Local client started
Processing Doom (Europe) from /mnt/roms/MAME/MAME - Software List ROMs/32x/doom.zip
Processing Motocross Championship (Europe) from /mnt/roms/MAME/MAME - Software List ROMs/32x/motox.zip
Processing Space Harrier (Europe) from /mnt/roms/MAME/MAME - Software List ROMs/32x/sharrier.zip
Processing Star Wars Arcade (Europe) from /mnt/roms/MAME/MAME - Software List ROMs/32x/swa.zip
Processing Toughman Contest (Europe, USA) from /mnt/roms/MAME/MAME - Software List ROMs/32x/toughman.zip
```