# Three.js Blender Export

Exports Three.js' ASCII JSON format.

## IMPORTANT

The exporter (r69 and earlier) has been completely replaced. Please ensure you have removed the io_three_mesh addon from your Blender addons directory before installing the current addon (io_three).

**Morph Target Exports** - currently returns an empty array `Return []` This needs to be reworked.
**Export Options UI** - currently no longer functions and also needs to be reworked. The export to threejs/json currenly works via passing true to all options.

## Installation

Recommended Blender version **This Branch is for Blender 3.6 - 4.2 I'll update this as more testing is done**

Copy the io_three folder to the scripts/addons folder. If it doesn't exist, create it. The full path is OS-dependent (see below).

Once that is done, you need to activate the plugin. Open Blender preferences, look for
Addons, search for `three`, enable the checkbox next to the `Import-Export: Three.js Format` entry.

Goto Usage.

### Windows

Should look like this:

3.6 - C:\Program Files\Blender Foundation\Blender\3.6\scripts\addons

4.2 - C:\Program Files\Blender Foundation\Blender 4.2\4.2\scripts\addons_core

### OSX

In your user's library for user installed Blender addons:

/Users/(myuser)/Library/Application Support/Blender/3.6X/scripts/addons

### Linux

By default, this should look like:

    /home/USERNAME/.config/blender 4.2/4.2X/scripts/addons_core

For Ubuntu users who installed Blender 4.2 via apt-get, this is the location:

    /usr/lib/blender/scripts/addons

## Usage

Activate the Import-Export addon under "User Preferences" > "Addons" and then use the regular Export menu within Blender, select `Three.js (json)`.

## Enabling msgpack

To enable msgpack compression copy the msgpack to scripts/modules.

## Importer

Currently there is no import functionality available.
