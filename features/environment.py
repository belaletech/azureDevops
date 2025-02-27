from behave.model_core import Status
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import os
import json

print(f'LT_BUILD_NAME: {os.environ.get("LT_BUILD_NAME")}')

INDEX = int(os.environ.get('INDEX', 0))
lt_build_name = os.getenv("LT_BUILD_NAME", "Default_Build_Name")
print(f"Using LT_BUILD_NAME: {lt_build_name}")

if os.environ.get("env") == "jenkins":
    desired_cap_dict = os.environ.get("LT_BROWSERS", "{}")
    CONFIG = json.loads(desired_cap_dict)
else:
    json_file = "config/config.json"
    try:
        with open(json_file) as data_file:
            CONFIG = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading config file: {str(e)}")
        CONFIG = []

username = os.getenv("LT_USERNAME", "belalahmad")
authkey = os.getenv("LT_ACCESS_KEY", "LT_UzeFPtk5kc9Z9eQSKXiqztgW3Tkx7lUfh0phyHFXWFQjbfp")


def before_scenario(context, scenario):
    try:
        if INDEX >= len(CONFIG):
            raise IndexError("INDEX out of range for CONFIG")
        
        desired_cap = setup_desired_cap(CONFIG[INDEX])

        if 'Chrome' in scenario.tags:
            options = ChromeOptions()
            options.browser_version = desired_cap.get("version", "latest")
            options.platform_name = desired_cap.get("platform", "Windows 11")
        elif 'Firefox' in scenario.tags:
            options = FirefoxOptions()
            options.browser_version = desired_cap.get("version", "latest")
            options.platform_name = desired_cap.get("platform", "Windows 10")
        elif 'Edge' in scenario.tags:
            options = EdgeOptions()
            options.browser_version = desired_cap.get("version", "latest")
            options.platform_name = desired_cap.get("platform", "Windows 8")
        else:
            raise ValueError("Unsupported browser tag")

        options.set_capability('build', lt_build_name)
        options.set_capability('name', desired_cap.get('name', 'Unnamed Scenario'))

        print("Browser Options:", options.to_capabilities())

        context.browser = webdriver.Remote(
            command_executor=f"https://{username}:{authkey}@hub.lambdatest.com/wd/hub",
            options=options
        )
    except Exception as e:
        print(f"Error in before_scenario: {str(e)}")
        context.scenario.skip(reason=f"Failed to initialize browser: {str(e)}")


def after_scenario(context, scenario):
    if hasattr(context, 'browser'):
        try:
            status = 'failed' if scenario.status == Status.failed else 'passed'
            context.browser.execute_script(f"lambda-status={status}")
        except Exception as e:
            print(f"Error setting lambda status: {str(e)}")
        finally:
            context.browser.quit()


def setup_desired_cap(desired_cap):
    cleaned_cap = {}
    for key, value in desired_cap.items():
        if key == 'connect' and not isinstance(value, (int, float)):
            cleaned_cap[key] = None
        else:
            cleaned_cap[key] = value
    return cleaned_cap
