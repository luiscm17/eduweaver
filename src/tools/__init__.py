"""
Tools Module

Contains utilities and properties for custom tools.
"""

from .web_search_properties import (
    get_academic_search_properties,
    get_general_search_properties,
    get_location_based_search_properties,
    get_research_search_properties
)

__all__ = [
    "get_academic_search_properties",
    "get_general_search_properties", 
    "get_location_based_search_properties",
    "get_research_search_properties"
]
