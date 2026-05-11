import os
import sys
import requests
import configparser

modsource = ""  # Hauptordner für alle Mods zwischen Profilen
gamepath = ""  # Standardmäßig Steam, wählbar zwischen Profilen
configpath = ""  # Auf Windows unter AppData/LocalLow/Ludgeon Studios

# Eine Directory mit den einzelnen Profilen, Configs etc
__file__

def true_last_mod(path) -> int:
    """Echte letzte Aktualisierung eines Ordners"""
    st_max = 0
    for root, dirs, files, rootfd in os.fwalk(path):
        st_max = max([os.stat(name, dir_fd=rootfd).st_mtime for name in files], st_max)
    return st_max

def id_translate(sws_id: str, force: bool = False) -> str:
    """Übersetzt eine Workshop-ID in den Namen der Mod"""
    try:
        with open("namecache.txt", mode="r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    cache = {x.split(";")[0]: x.split(";")[1] for x in lines}
    if force or sws_id not in cache.keys():
        res = requests.get("https://steamcommunity.com/sharedfiles/filedetails/?id=" + sws_id)
        try:
            title = res.text.split("<title>")[1].split("<title/>")[0]
        except Exception:
            title = None
        if title is not None:
            cache[sws_id] = title
            with open("namecache.txt", mode="a") as f:
                f.writelines([sws_id + ";" + title])
    else:
        title = cache[sws_id]
    return title

def parse_command(inp: str) -> tuple(str, ...):
    intext = False
    escaped = False
    new = False
    ls = [""]
    for c in inp.strip():
        if c == "\\":
            if not escaped:
                escaped = True
            else:
                escaped = False
                ls[-1] += "\\"
        elif c == '"':
            if escaped:
                ls[-1] += c
            else:
                intext = not intext
        elif c == " ":
            if escaped or intext:
                ls[-1] += " "
            elif not new:
                new = True
                ls.append("")
        else:
            ls[-1] += c
        if new and c != " ":
            new = False
        if escaped and c != "\\":
            escaped = False
        

# Current ist Standard, Blank als special profile

# Bei einem Switch auf ein Profil, jetzige Einstellungen abspeichern und merken
# Möglichkeit, bestehendes Profil zu duplizieren

if __name__ == "__main__":
    while True:
        print("DaimCo RW-ProfileMan\n")
        # Hi
        print(f"""
        A profile consists of a Gamepath, a Configlist and a Modlist
        p = Profile (Standard) | c = Config | m = Mods | g = Game
        ch [p|c|m|g] <id> | Change currently used Profile
        ls [p|c|m|g] | List Profiles
        dp [p|c|m] [id] | Duplicate Profile
        rn [p|c|m|g] [id] <new_id> | Rename Profile
        remove <p|c|m|g> <id> | Delete Profile
        addgame [g] [path] | Add a game directory to the list of available games
        sv [p|c|m] <id> | Manually overwrite a saved profile with the currently active one
        start [p] [id] | Start the specified profile
        q | Quit
        -------------------------""")
        t_in = input("-->")
        args = t_in.strip().split()
