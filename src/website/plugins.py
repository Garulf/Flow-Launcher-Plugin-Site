from dataclasses import dataclass

import requests

MANIFEST_URL = 'https://raw.githubusercontent.com/Flow-Launcher/Flow.Launcher.PluginsManifest/plugin_api_v2/plugins.json'


@dataclass
class Plugin:
    ID: str
    Name: str
    Description: str
    Author: str
    Version: str
    Language: str
    Website: str
    UrlDownload: str
    UrlSourceCode: str
    IcoPath: str
    LatestReleaseDate: str
    DateAdded: str
    Tested: bool = None
    ActionKeyword: str = None


def get_plugins():
    response = requests.get(MANIFEST_URL)
    response.raise_for_status()
    return [Plugin(**plugin) for plugin in response.json()]
