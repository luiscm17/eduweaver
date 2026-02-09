"""
Web Search Additional Properties

Module to define custom additional properties for HostedWebSearchTool.
"""

def get_academic_search_properties(user_location: dict = None, preferred_domains: list = None):
    """
    Properties for academic search
    
    Args:
        user_location: Dictionary with user location
        preferred_domains: List of preferred domains
    
    Returns:
        dict: Properties configured for academic search
    """
    properties = {}
    
    # Contexto geográfico
    if user_location:
        properties["user_location"] = user_location
    
    # Preferencias de dominio académico
    if preferred_domains:
        properties["domain_preferences"] = {
            "preferred_domains": preferred_domains,
            "academic_sources": True,
            "excluded_domains": ["social_media", "forums", "spam"]
        }
    
    # Contexto de búsqueda académica
    properties["search_context"] = {
        "time_range": "last_30_days",
        "source_types": ["academic", "research", "official_docs"],
        "content_filter": "high_quality"
    }
    
    # Contexto de aplicación
    properties["application_context"] = {
        "purpose": "academic_research",
        "field": "technology_science",
        "credibility_level": "academic"
    }
    
    return properties


def get_general_search_properties(user_location: dict = None):
    """
    Properties for general search
    
    Args:
        user_location: Dictionary with user location
    
    Returns:
        dict: Properties configured for general search
    """
    properties = {}
    
    # Contexto geográfico
    if user_location:
        properties["user_location"] = user_location
    
    # Preferencias de búsqueda general
    properties["search_context"] = {
        "time_range": "last_7_days",
        "source_types": ["news", "web", "blogs"]
    }
    
    return properties


def get_location_based_search_properties(city: str, country: str = "US"):
    """
    Properties based on geographic location
    
    Args:
        city: City of the user
        country: Country of the user
    
    Returns:
        dict: Properties with location context
    """
    return {
        "user_location": {
            "city": city,
            "country": country
        }
    }


def get_research_search_properties(field: str = "technology_science"):
    """
    Properties for specialized research
    
    Args:
        field: Research field
    
    Returns:
        dict: Properties for specialized research
    """
    return {
        "application_context": {
            "purpose": "research",
            "field": field,
            "credibility_level": "academic"
        },
        "domain_preferences": {
            "preferred_domains": ["edu", "gov", "org", "ieee.org", "acm.org"],
            "academic_sources": True
        },
        "search_context": {
            "time_range": "last_30_days",
            "source_types": ["academic", "research", "official_docs"]
        }
    }
