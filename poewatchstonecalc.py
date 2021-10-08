from poepy_core import GetWatchstoneData

download_mode = True

league_name = r"Harvest"


max_watchstone_data = {
    "Booming Populace": 15,
    "Irresistable Temptation": 18,
    "Misinformation": 12,
    "Stalwart Defenders": 12,
    "Territories Unknown": 18,
    "Terror": 12,
    "War Among the Stars": 12,
}


watchstone_data = GetWatchstoneData(league_name, download_mode)

for item in watchstone_data:
    item_name = item.get("name")
    item_variant = int(item.get("variant"))
    if (
        item_name in max_watchstone_data
        and max_watchstone_data[item_name] == item_variant
    ):
        print(item_name, item.get("variant"), item.get("chaosValue"))
