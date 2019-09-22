#! python3.6

import json
import time
import timeit
from statistics import mean
from textwrap import dedent, indent
from timeit import default_timer as timer
from typing import Any, Callable, Dict, List, Set

import regex
import requests
import requests_cache

import poetiergen_constants as constants

requests_cache.install_cache("ninja_data", expire_after=172800)


class MeanTimer:
    def __init__(self, name=None):
        self.name = " '" + name + "'" if name else ""
        self.times: List[float] = []

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (timeit.default_timer() - self.start) * 1000.0
        self.times.append(self.took)
        print(
            "Code block" + self.name + " took: " + str(mean(self.times)) + "(mean) ms"
        )


def FileToJson(filepath: str) -> List[dict]:
    file_data = ""
    with open(filepath, "r", encoding="utf-8") as json_file:
        file_data = json_file.read()
    return json.loads(file_data).get("lines")


# MORE URL PARAMS: Essences: 'Essence', Currency: 'Currency', Fragments: 'Fragment', Scarabs: 'Scarab', Fossils: 'Fossil', Resonators: 'Resonator'


def DownloadJson(
    league_param: str, type_param: str, use_cache: bool = True, type_: str = "item"
) -> List[Dict]:
    payload = {"league": league_param, "type": type_param}
    if use_cache:
        r = requests.get(f"https://poe.ninja/api/data/{type_}overview", params=payload)
        print(f"Downloaded from: {r.url} - Cache: {r.from_cache}")  # type: ignore
    else:
        with requests_cache.disabled():
            r = requests.get(
                f"https://poe.ninja/api/data/{type_}overview", params=payload
            )
            print(f"Downloaded from: {r.url} - Cache: False")  # type: ignore

    r.encoding = "utf-8"
    return r.json().get("lines")


def GetDivinationData(
    league: str = None, download: bool = False, use_cache: bool = True
) -> List[dict]:
    if download and league is not None:
        print("Starting Download...")
        div_data = DownloadJson(league, "DivinationCard", use_cache)
        print("Download complete.")
    else:
        div_data = FileToJson(constants.json_div_filepath)
    return div_data


def GetFragmentData(
    league: str = None, download: bool = False, use_cache: bool = True
) -> List[dict]:
    if download and league is not None:
        print("Starting Download...")
        fragment_data = DownloadJson(league, "Fragment", use_cache, "currency")
        print("Download complete.")
    else:
        fragment_data = FileToJson(constants.json_fragments_filepath)
    return fragment_data


def GetBasesData(
    league: str = None, download: bool = False, use_cache: bool = True
) -> List[dict]:
    if download and league is not None:
        print(f"Starting Download...")
        bases = DownloadJson(league, "BaseType", use_cache)
        print("Download complete.")
    else:
        bases = FileToJson(constants.json_bases_filepath)
    return bases


def GetUniquesData(
    league: str = None, download: bool = False, use_cache: bool = True
) -> List[List[dict]]:
    uniques_data = []
    param_uniques = [
        "UniqueArmour",
        "UniqueWeapon",
        "UniqueFlask",
        "UniqueAccessory",
        "UniqueJewel",
        "UniqueMap",
    ]
    if download and league is not None:
        print("Starting Download...")
        for param in param_uniques:
            uniques_data.append(DownloadJson(league, param, use_cache))
        print("Download complete.")
    else:
        for path in constants.json_unique_filepaths:
            uniques_data.append(FileToJson(path))
    return uniques_data


def write_to_file(file_path: str, write_string: Any) -> None:
    with open(file_path, "w") as target_file:
        target_file.write(str(write_string))


def BaseTypeString(base_types: list) -> str:
    """
    Return a space-joined string of the input list,
    with each list entry pre- and suffixed by \"
    """
    return " ".join(f'"{base_type}"' for base_type in base_types).strip()


def quicktime(fun: Callable) -> float:
    start = timer()
    fun()
    end = timer()
    print(end - start)
    return end - start


def ternary(condition: bool, true_value: Any, false_value: Any = 0) -> Any:
    return true_value if condition else false_value


def InvestigatedItem(item):
    inv_set = {  # type: ignore
        # ('Marble Amulet', 86, 'Normal'),
        # ('Prismatic Ring', 82, 'Shaper'),
        # ('Latticed Ringmail', 84, 'Elder'),
        # ('Leatherscale Boots', 82, 'Elder'),
        # ('Bone Helmet', 86, 'Elder'),
        # ('Opal Ring', 85, 'Elder'),
        # ('Eternal Burgonet', 84, 'Elder')
        # ('Titanium Spirit Shield', 86, 'Shaper')
        # ('Driftwood Sceptre', 82, 'Normal'),
        # ('Highland Blade', 82, 'Normal')
        # ('Marble Amulet', 'Normal'),
        # ('Prismatic Ring', 'Shaper'),
        # ('Latticed Ringmail', 'Elder'),
        # ('Leatherscale Boots', 'Elder'),
        # ('Bone Helmet', 'Elder'),
        # ('Opal Ring', 'Elder'),
        # ('Eternal Burgonet', 'Elder'),
        # ('Titanium Spirit Shield', 'Shaper'),
        # ('Driftwood Sceptre', 'Normal'),
        # ('Highland Blade', 'Normal')
    }
    return item in inv_set
