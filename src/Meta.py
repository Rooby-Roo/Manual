
from BaseClasses import Tutorial
from worlds.AutoWorld import World, WebWorld
from .hooks.Data import hook_early_modify_world_properties
from .Data import meta_table

enable_region_diagram = meta_table.get("enable_region_diagram", False)

def set_world_attributes(world_properties: dict) -> dict:
    world_properties['description'] = set_world_doc(world_properties.get('description'))
    world_properties['webworld'] = set_world_webworld(world_properties.get('webworld'))
    world_properties = hook_early_modify_world_properties(world_properties)
    return world_properties

def set_world_doc(base_doc: str):
    if meta_table.get("docs", {}).get("apworld_description", []):
        fullstring = ""
        for line in meta_table["docs"]["apworld_description"]:
            fullstring += "\n" + line
        base_doc = fullstring
    return base_doc

def set_world_webworld(web: WebWorld) -> WebWorld:
    if meta_table.get("docs", {}).get("web", {}):
        Web_Config = meta_table["docs"]["web"]

        web.theme = Web_Config.get("theme", web.theme)
        web.game_info_languages = Web_Config.get("game_info_languages", web.game_info_languages)
        web.options_presets = Web_Config.get("options_presets", web.options_presets)
        web.options_page = Web_Config.get("options_page", web.options_page)
        if hasattr(web, 'bug_report_page'):
            web.bug_report_page = Web_Config.get("bug_report_page", web.bug_report_page)
        else:
            web.bug_report_page = Web_Config.get("bug_report_page", None)

        if Web_Config.get("tutorials", []):
            tutorials = []
            for tutorial in Web_Config.get("tutorials", []):
                tutorials.append(Tutorial(
                    tutorial.get("name", "Multiworld Setup Guide"),
                    tutorial.get("description", "A guide to setting up manual game integration for Archipelago multiworld games."),
                    tutorial.get("language", "English"),
                    tutorial.get("file_name", "setup_en.md"),
                    tutorial.get("link", "setup/en"),
                    tutorial.get("authors", [meta_table.get("creator", meta_table.get("player", "Unknown"))])
                ))
            web.tutorials = tutorials
    return web