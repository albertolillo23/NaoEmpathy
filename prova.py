import json

with open("colors.json", "r") as f:
    colors = json.load(f)
    print(colors)
    print(colors[""])