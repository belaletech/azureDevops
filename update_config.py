import os
import json

# Load the config file
with open("config.json", "r") as file:
    config = json.load(file)

# Replace LT_BUILD_NAME dynamically
for capability in config:
    capability["build"] = os.getenv("LT_BUILD_NAME", "Default Build Name")  # Fallback if env variable is not set

# Save the modified config
with open("updated_config.json", "w") as file:
    json.dump(config, file, indent=2)

print("Updated capabilities file:", json.dumps(config, indent=2))
