#! python3.6
from poepy_core import GetFragmentData

download_mode = True

league_name = r"Ultimatum"

price_data = {
    "Chayula": {"pure": 0, "base": 0},
    "Tul": {"pure": 0, "base": 0},
    "Uul-Netol": {"pure": 0, "base": 0},
    "Esh": {"pure": 0, "base": 0},
    "Xoph": {"pure": 0, "base": 0},
}

empowerment = ["Pure", "Enriched", "Charged"]


def ProcessJsonData(data):

    for item in data:
        item_name = item.get("currencyTypeName")
        if any(item_name.startswith(prefix) for prefix in price_data.keys()):
            item_price = item.get("receive").get("value")
            breachlord = item_name.split(" ")[0].replace("'s", "")
            if "Pure" in item_name:
                price_data[breachlord]["pure"] = item_price
            elif not any(upgrade in item_name for upgrade in empowerment):
                price_data[breachlord]["base"] = item_price
    for stone in price_data:
        pure_value = price_data[stone]["pure"]
        base_value = price_data[stone]["base"]
        upgrade_value = price_data[stone]["pure"] - price_data[stone]["base"]
        print(stone, upgrade_value, base_value, pure_value)


fragment_data = GetFragmentData(league_name, download_mode)
ProcessJsonData(fragment_data)
