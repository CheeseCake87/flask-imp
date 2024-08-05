from dataclasses import dataclass


@dataclass
class Config:
    latest = 'v5'
    versions = ['v3', 'v4', 'v5']
