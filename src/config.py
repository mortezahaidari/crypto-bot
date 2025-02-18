import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Load and validate bot configuration from YAML file
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        dict: Validated configuration dictionary
    """
    # Load environment variables first
    load_dotenv()
    
    # Resolve absolute path
    base_dir = Path(__file__).parent.parent
    config_file = base_dir / config_path
    
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    with open(config_file) as f:
        config = yaml.safe_load(f)
    
    # Validate essential sections
    required_sections = ['strategy', 'exchange', 'risk_params']
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: {section}")
    
    return config