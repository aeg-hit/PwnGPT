import os
import getpass



def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var]=getpass.getpass(f"{var}:")



if __name__ == "__main__":
    _set_env("OPENAI_API_KEY")
