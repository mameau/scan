# scan
mame scanner in python

1. create the main config pointing to your roms
2. create a config for a system
3. pass that system to `scan.py`


```
./scan.py --system mamesl --cfg psx --mode file-parent --output-mode pegasus
./scan.py --system mamesl --cfg 32x --mode file --output-mode json
./scan.py --system generic --cfg xbox --mode file --output-mode json
```
