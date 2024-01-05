import requests
import pandas as pd


def intensity_extract(config: dict):
    """Retrieves information from Carbon Intensity REST API regional intensity.

    Get Carbon Intensity data between the {from} and {to} datetimes. 
    The maximum date range is limited to 14 days. All times provided in UTC (+00:00).

    For up to date information visit: 
    https://carbon-intensity.github.io/api-definitions/#get-intensity-from-pt24h


    Args:
        config (dict): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    headers = {"Accept": "application/json"}
    region = config.get("region", 17)  # Defaults to 17 (Wales)
    from_date = config["from_date"]  # Mandatory field
    to_date = config["to_date"]  # Mandatory field
    url = (
        "https://api.carbonintensity.org.uk/regional/intensity/"
        + f"{from_date}/{to_date}/regionid/{region}"
    )
    r = requests.get(url, params={}, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise Exception(f"Extraction failed with code: ${r.status_code}")


def intensity_transform(data, config: dict = {}):
    lst_data = []
    cols = ["from_date", "to_date", "actual", "forecast"]

    for s in data["data"]["data"]:
        lst_data.append(
            [
                s["from"],
                s["to"],
                s.get("intensity", {}).get("actual", None),
                s.get("intensity", {}).get("forecast", None),
            ]
        )

    df = pd.DataFrame(data=lst_data, columns=cols)
    df["regionid"] = data["data"]["regionid"]
    df["dnoregion"] = data["data"]["dnoregion"]
    df["shortname"] = data["data"]["shortname"]
    return df
