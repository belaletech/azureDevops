import json
import os

# Load the config file
with open("config.json", "r") as file:
    config = json.load(file)

# Replace the build name dynamically
for item in config:
    item["build"] = os.getenv("LT_BUILD_NAME", "Default Build Name")  # Fallback if env var is missing

# Save the updated config
with open("config.json", "w") as file:
    json.dump(config, file, indent=2)

print("Updated config.json with LT_BUILD_NAME:", os.getenv("LT_BUILD_NAME"))
