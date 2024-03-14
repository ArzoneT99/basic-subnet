import pytest

def pytest_collection_modifyitems(config, items):
    # Add the 'subnet' marker to all test items
    for item in items:
        item.add_marker('subnet')