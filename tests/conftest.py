# conftest.py
import pytest
import os

def pytest_sessionstart(session):
    os.chdir(os.path.abspath('/github.workspace'))