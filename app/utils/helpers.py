"""Utility functions"""
import logging
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    """
    Setup application logger
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger


def format_currency(amount: float) -> str:
    """
    Format currency
    
    Args:
        amount: Amount in thousands
        
    Returns:
        Formatted string
    """
    return f"${amount:,.0f}k"


def get_timestamp() -> str:
    """
    Get current timestamp
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
