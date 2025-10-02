import json
import requests
from typing import Any


API_URL = "https://api.api-ninjas.com/v1/animals"
ANIMALS_FILE_PATH = "animals_data.json"


def load_data(file_path: str) -> Any:
    """Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        Any: Parsed Python object (list or dict).
    """
    with open(file_path, "r", encoding="UTF-8") as handle:
        return json.load(handle)


def fetch_animals_from_api(animal_name: str, api_key: str) -> list[dict]:
    """Fetch animal data from the API-Ninjas API.

    Args:
        animal_name (str): Name of the animal to search for.
        api_key (str): API key for authentication.

    Returns:
        list[dict]: List of animal dictionaries from the API.

    Raises:
        requests.RequestException: If the API request fails.
        ValueError: If the API returns an error or no data.
    """
    headers = {"X-Api-Key": api_key}
    params = {"name": animal_name}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, list):
            raise ValueError(f"Unexpected API response format: {type(data)}")

        return data
    except requests.exceptions.RequestException as e:
        raise requests.RequestException(f"API request failed: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse API response: {e}") from e


def fetch_data(
    animal_name: str, api_key: str | None = None, use_json: bool = False
) -> list[dict]:
    """
    Fetches the animals data for the animal 'animal_name'.

    Args:
        animal_name (str): Name of the animal to search for.
        api_key (str, optional): API key for API-Ninjas. Required if use_json=False.
        use_json (bool): If True, load data from JSON file instead of API.

    Returns:
        list[dict]: A list of animals, each animal is a dictionary:
        {
            'name': ...,
            'taxonomy': {
                ...
            },
            'locations': [
                ...
            ],
            'characteristics': {
                ...
            }
        }

    Raises:
        ValueError: If API key is required but not provided, or if animal_name is empty.
        FileNotFoundError: If JSON file is not found when use_json=True.
        requests.RequestException: If API request fails.
    """
    if not animal_name or not animal_name.strip():
        raise ValueError("Animal name cannot be empty")

    if use_json:
        return load_data(ANIMALS_FILE_PATH)
    else:
        if not api_key:
            raise ValueError("API key is required for API mode")
        return fetch_animals_from_api(animal_name, api_key)
