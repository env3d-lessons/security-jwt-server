import os
import pathlib
import pytest
import time
import subprocess
import signal
import shutil


bad_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
expired_jwt = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg3YmJlMDgxNWIwNjRlNmQ0NDljYWM5OTlmMGU1MGU3MmEzZTQzNzQiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MDc0MDg3MTgxOTIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTA2OTE2MjE1OTUyMjY5MzI0MTAiLCJlbWFpbCI6ImptYWRhckBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6IjFsN19WNFgtQThvSThrLVNzVjQxZ0EiLCJuYW1lIjoiSmFzb24gTWFkYXIiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jSnhIc0NON1p4OHpTb1QxSnpNbzlQYTVQT2ZIdVZCVFV1bHN1VEYxN1lfOWJ4S0k1bnQ9czk2LWMiLCJnaXZlbl9uYW1lIjoiSmFzb24iLCJmYW1pbHlfbmFtZSI6Ik1hZGFyIiwiaWF0IjoxNzIwNjcwODA5LCJleHAiOjE3MjA2NzQ0MDl9.JrcEdS1hbgvlj2idiP2up5MCNRyjuUoPW49FWyOANnrofryTNlfrxlUeAgn3zozeWw8ZMsySTJJZ9Jd2SC7C1-riV7lr100Kokje-YPvgLLJQZhvefFTLRXYQyZ8ETbKOAox9Iwc_QjeC7MPyWgF88kXqYPJ8y-UHN66B2X9_X_JVPn7JJ5wE-F5gkSf_23bAGjb2wshMgQYElc7JsINy5ZqhIaJncVuIn1SYfzgSVJcPDyFsKQ4mIy-l7kO7SSTYWq8WdJXKh6eX-ZYHV8o6DLWy932L8yWZfk9bjqKat6ysYJ-xaES2BS5YMIT2IS_HEpa_hN4jq4jKlzq1SxLoA"

@pytest.fixture(scope="session")
def start_app():
    script_path = os.path.abspath("index.js")
    script_dir = os.path.dirname(script_path)
    node_path = shutil.which('node')
    print(script_dir, script_path, node_path)
    p = subprocess.Popen([node_path, script_path], cwd=script_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(2)
    print(p.stdout.readline())
    yield p
    # Gracefully terminate the process and its children
    if p.poll() is None:  # Check if process is still running
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)  # Kill process group
        time.sleep(2)  # Give it time to terminate
        if p.poll() is None:  # If still running, force kill
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)

def test_with_no_jwt(start_app):
    content = os.popen('curl -s --head localhost:8080/info').read()
    assert 'Unauthorized' in content

def test_with_bad_jwt(start_app):
    content = os.popen(f'curl -s --head -H "Authorization: Bearer {bad_jwt}" localhost:8080/info').read()
    assert 'Unauthorized' in content

def test_with_expired_jwt(start_app):
    content = os.popen(f'curl -s --head -H "Authorization: Bearer {expired_jwt}" localhost:8080/info').read()
    assert 'Unauthorized' in content

def test_with_valid_jwt(start_app):
    with open('jwt.txt') as f:
        jwt = f.read().strip()
        content = os.popen(f'curl -s --head -H "Authorization: Bearer {jwt}" localhost:8080/info').read()
        assert '200' in content

