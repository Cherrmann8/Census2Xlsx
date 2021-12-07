import sys
import getopt
import json
import censusdata

# Global Variables
censusType = "acs5"
censusYear = 2019


# DETAIL
# PROFILE
# geo_code = censusdata.censusgeo(
#     [("state", "06"), ("zip code tabulation area", "90002")]
# )

# SUBJECT
# geo_code = censusdata.censusgeo([("zip code tabulation area", "90002")])

# geo_code = censusdata.censusgeo([("state", "04"), ("county", "004")])

# print(geo_code)
# print(geo_code.sumlevel())

# downloaded_data = censusdata.download(
#     censusType,
#     censusYear,
#     geo_code,
#     ["DP05_0038PE"],
#     tabletype="profile",
# )

# downloaded_data = downloaded_data.to_dict()
# print(downloaded_data)

geos = censusdata.geographies(
    censusdata.censusgeo([("state", "05"), ("county", "007")]), "acs5", 2018
)
g_keys = list(geos.keys())
g_keys.sort()
for key in g_keys:
    print(key, "-", geos[key])
