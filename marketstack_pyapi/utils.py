from dotenv import dotenv_values


def load_env_variables() -> dict[str, str]:
    return dotenv_values()
