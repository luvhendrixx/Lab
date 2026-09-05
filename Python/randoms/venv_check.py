import os
import sys
from pathlib import Path


def check_venv():
    is_active_prefix = sys.prefix != sys.base_prefix

    is_active_env_var = "VIRTUAL_ENV" in os.environ

    if is_active_prefix or is_active_env_var:
        print("✅ Virtual env is ACTIVE.")
        print(f"Path: {sys.prefix}")
    else:
        print("⁉️ No venv is active (Using global/system python")


def is_uv_env():
    cfg_path = Path(sys.prefix) / "pyvenv.cfg"

    if cfg_path.exists():
        with open(cfg_path, "r") as file:
            content = file.read()
            if "uv =" in content:
                return True
    else:
        return False


def main():
    catch = is_uv_env()
    if catch == True:
        print("👍 This env was created and managed by uv")
    else:
        print("🫪 This env is the std env (NOT MANAGED/CREATED BY UV)")


if __name__ == "__main__":
    check_venv()
    main()
