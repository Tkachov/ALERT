# ALERT: Amazing Luna Engine Research Tools

This repository contains Python scripts written to research Insomniac Games' games assets formats.

Specifically, the games are:
- Sunset Overdrive;
- Marvel's Spider-Man Remastered;
- Marvel's Spider-Man: Miles Morales;
- Ratchet & Clank: Rift Apart;
- Marvel's Spider-Man 2;
- Marvel's Wolverine.

Scripts were mostly written for MSMR, MM and RCRA, with some support of SO added later. Scripts most likely would work with MSM2 and MW, though some minor changes could be required.

The repo could be roughly split into three parts:
- **dat1lib/** — a "library" that allows to load assets to work with or modify and save them;
- **server/** — Assets Browser, a web UI application to explore game's archives and view assets contents (ranging from raw hex to specialized viewers);
- standalone scripts that use the library to do different useful actions with the assets.

## Assets Browser

![Assets Browser screenshot](https://github.com/Tkachov/ALERT/assets/1948111/8f96a428-94d5-4337-9d07-0dc8394b80f9)

Web app that allows to browse games' assets, view or extract them, export to stage, compare/diff and see other assets they reference. There are special viewers for .model, .texture and .nodegraph, and an option to view any asset's sections in text representation (on in hex view, if there is no implementation made for this section).

Built .exe can be found in the [Releases](https://github.com/Tkachov/ALERT/releases).

## Scripts

Some of the most interesting ones:

- **model_to_ascii.py** and **ascii_to_model.py** — converters of .model format to .ascii and back. Well, not exactly converters since .ascii can't hold all of the information from .model (nor all of it is researched), and modified .model is made by injecting .ascii into the original .model;
- **spiderman_pc_model.py** and **spiderman_pc_mi.py** — wrappers around previous two, so the arguments and behavior matches similarly named closed-source tools by ID-Daemon;
- **model_to_gltf.py** and **gltf_to_model.py** — similar to the first two, but for .gltf format. Allows to also extract shapekeys;
- **animclip_to_gltf.py** — makes a GLTF by applying base state of .animclip to .model. .animclip support is poor;
- **dsar_codec.py** — compresses to or decompresses from DSAR archive format;
- **change_soundbank.py** — can be used to inject modified .bnk into .soundbank.

## Usage

Contents of this repo are mostly for researchers, who can read the code, fix it if it doesn't work the way they want and write their own tools based on it. Some experienced mod makers could also find it useful. For mod users, this is unlikely to be needed.

Assets Browser and some of the scripts are packed into a Windows .exe that can be found in [Releases](https://github.com/Tkachov/ALERT/releases). That's an easy way of using these in case you don't know how to run Python scripts and don't intend to edit the code, yet would like to use these for something. Just run .exe, open [localhost:55555](http://localhost:55555/) in your browser and type path to your 'toc' to get started.

Otherwise, just clone the repo and run scripts with Python. I'm usually doing that from Ubuntu on Windows, but normal Windows build of Python should also work fine. For Assets Browser, you'd need Flask package installed. Some scripts could require installing additional packages too, like pygltflib or lz4.

## License

Like [Overstrike](https://github.com/Tkachov/Overstrike), this code is under GPLv3 license. You're free to build whatever you like on top of it, but your code needs to be released under the same license.
