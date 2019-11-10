# Python script to convert GlobalCache IR database files to broadlink IR codes
The package contains a python script that can operate on files downloaded from GlobalCache at https://irdb.globalcache.com/Home/Database

Running the python script outputs the command name and the corresponding broadlink command one per line.

## Usage
`python gc2broadlink.py <<codefile>>`
where codefile is the file downloaded from GlobalCache

A sample GlobalCache IR code file to control most Vizio TVs is included in the package and can be run to see the sample output

`python gc2broadlink.py VizioTV.gccodes`

## Using with broadlink-mqtt
The commands that are generated are compatible with broadlink-mqtt https://github.com/eschava/broadlink-mqtt

The `cmds.awk` script can be used to automatically generate commands to be consumed by `mqtt.py`

### Usage
Pipe the output of `gc2broadlink.py` into awk script as follows
`python gc2broadlink.py downloaded_code_file | awk -f cmds.awk -v command_dir=/path/to/broadlink-mqtt/commands -v device=yourdevicename`

Replace the downloaded_code_file, path to commands and yourdevicename as appropriate

The above example command will generate appropriate files in the `/path/to/broadlink-mqtt/commands/yourdevicename` that can be consumed by mqtt.py

