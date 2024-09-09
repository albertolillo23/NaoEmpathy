import json

best_emotion = "neutral"

with open("colors.json", "r") as f:
    colors = json.load(f)
    print(colors)
    print(colors[best_emotion][0])