"""Exports for symkan's pruning and attribution module.

This module exposes fault-tolerant feature attribution entry points.
"""

from .attribution import safe_attribute, safe_attribute_report

__all__ = ["safe_attribute", "safe_attribute_report"]
