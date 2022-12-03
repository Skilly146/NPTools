import utils


game_name = ''
game_number, api_key = utils.credentials(game_name)
scanning_data = utils.call_api(game_number, api_key)
converted_dict = {"stars": []}
key_order = ["uid", "name", "x", "y", "r", "ga", "e", "i", "s", "st", "puid", "wh"]
for star in scanning_data["stars"]:
    cur_star_dict = {}
    for field in key_order:
        if field == "name":
            cur_star_dict["name"] = scanning_data["stars"][star]["n"]
        elif field == "x" or field == "y":
            cur_star_dict[field] = float(scanning_data["stars"][star][field])
        else:
            try:
                cur_star_dict[field] = int(scanning_data["stars"][star][field])
            except KeyError:
                continue
    converted_dict["stars"].append(cur_star_dict)

string_converted_dict = ""
for char in str(converted_dict):
    if char == "'":
        string_converted_dict += '"'
    else:
        string_converted_dict += char

print(string_converted_dict)
