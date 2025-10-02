import json
import argparse
import sys
import requests
from pathlib import Path
from typing import Any, Generator

ANIMALS_FILE_PATH = "animals_data.json"
TEMPLATE_FILE_PATH = "animals_template.html"
API_URL = "https://api.api-ninjas.com/v1/animals"


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
        raise ValueError(f"Failed to parse API response: {e}")


def load_text(file_path: str) -> str:
    """Load plain text content from a file.

    Args:
        file_path (str): Path to the text/HTML file.

    Returns:
        str: File content as a string.
    """
    with open(file_path, "r", encoding="UTF-8") as handle:
        return handle.read()


def save_data(file_name: str, content: str) -> None:
    """Save text content to a file in the current directory.

    Args:
        file_name (str): Name of the output file.
        content (str): Text to write.
    """
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(content)


def serialize_animal(animal: dict[str, Any]) -> str:
    """Serialize a single animal into an HTML card list item."""
    characteristics = animal.get("characteristics", {})
    locations = ", ".join(animal.get("locations", []))
    fields = [
        ("Diet", characteristics.get("diet", "")),
        ("Locations", locations),
        ("Type", characteristics.get("type", "")),
        ("Skin type", characteristics.get("skin_type", "")),
        ("Lifespan", characteristics.get("lifespan", "")),
        ("Weight", characteristics.get("weight", "")),
        ("Top speed", characteristics.get("top_speed", "")),
        ("Temperament", characteristics.get("temperament", "")),
    ]

    details = [
        f'            <li class="card__detail"><strong>{label}:</strong> {value}</li>'
        for label, value in fields
        if value
    ]

    lines = [
        '    <li class="cards__item">',
        f'        <div class="card__title">{animal.get("name", "")}</div>',
        '        <div class="card__text">',
        '            <ul class="card__details">',
        *details,
        "            </ul>",
        "        </div>",
        "    </li>",
    ]
    return "\n".join(lines)


def extract_skin_type(animal: dict[str, Any]) -> str:
    """Return normalized skin type value for an animal."""
    characteristics = animal.get("characteristics", {})
    return characteristics.get("skin_type") or "Unknown"


def list_skin_types(data: list[dict]) -> list[str]:
    """Collect available skin types, keeping 'Unknown' (if present) last."""
    values = {extract_skin_type(animal) for animal in data}
    known = sorted(value for value in values if value != "Unknown")
    if "Unknown" in values:
        known.append("Unknown")
    # Add "All" option at the beginning
    return ["All"] + known


def prompt_skin_type(options: list[str]) -> str:
    """Prompt the user to choose one of the available skin types."""
    lookup = {option.lower(): option for option in options}
    while True:
        choice = input("Enter a skin type (or its number): ").strip()
        if not choice:
            print("Please enter a value from the list.")
            continue
        if choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(options):
                return options[index - 1]
        normalized = lookup.get(choice.lower())
        if normalized:
            return normalized
        print("Invalid choice. Please use one of the listed skin types.")


def filter_by_skin_type(data: list[dict], skin_type: str) -> list[dict]:
    """Return only animals matching the selected skin type."""
    if skin_type == "All":
        return data
    return [animal for animal in data if extract_skin_type(animal) == skin_type]


def yield_data(data: list[dict]) -> Generator[str, None, None]:
    """Yield HTML list items for each animal in card format.

    Args:
        data (list[dict]): List of animal dictionaries.

    Yields:
        str: HTML string for one animal card.
    """
    for animal in data:
        yield serialize_animal(animal)


def create_error_message(animal_name: str) -> str:
    """Create an HTML error message for when no animals are found.

    Args:
        animal_name (str): The animal name that was searched for.

    Returns:
        str: HTML string with error message.
    """
    return f"""
    <li class="cards__item">
        <div class="card__title">No Results Found</div>
        <div class="card__text">
            <h2 style="color: #e74c3c; text-align: center; margin: 20px 0;">
                The animal "{animal_name}" doesn't exist.
            </h2>
            <p style="text-align: center; color: #7f8c8d; font-style: italic;">
                Please try searching for a different animal name.
            </p>
        </div>
    </li>
    """


def replace_html_content(template_file_path: str, placeholder: str, data: str) -> str:
    """Replace a placeholder in an HTML template with data.

    Args:
        template_file_path (str): Path to the HTML template.
        placeholder (str): Placeholder text to replace.
        data (str): Replacement content.

    Returns:
        str: Final HTML with replaced content.
    """
    template = load_text(template_file_path)
    return template.replace(placeholder, data)


def generate_html(
    *,
    data: list[dict],
    template_path: str,
    placeholder: str = "__REPLACE_ANIMALS_INFO__",
    skin_type: str | None = None,
) -> str:
    """Generate full HTML by optionally filtering and injecting list items.

    Args:
        data: Full dataset of animals.
        template_path: Path to HTML template file.
        placeholder: Template placeholder to replace.
        skin_type: Optional skin type to filter by.

    Returns:
        Final HTML string.
    """
    animals = data
    if skin_type and skin_type != "All":
        animals = filter_by_skin_type(data, skin_type)
        if not animals:
            raise ValueError(f"No animals found for skin type '{skin_type}'.")

    formatted_data = "\n".join(yield_data(animals))
    return replace_html_content(template_path, placeholder, formatted_data)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate animals HTML page.")
    parser.add_argument(
        "--data",
        default=ANIMALS_FILE_PATH,
        help="Path to animals JSON data (default: animals_data.json)",
    )
    parser.add_argument(
        "--template",
        default=TEMPLATE_FILE_PATH,
        help="Path to HTML template (default: animals_template.html)",
    )
    parser.add_argument(
        "--output",
        default="animals.html",
        help="Output HTML file path (default: animals.html)",
    )
    parser.add_argument(
        "--skin-type",
        dest="skin_type",
        help="Filter by skin type (skips interactive prompt). Use 'All' to show all skin types.",
    )
    parser.add_argument(
        "--list-skin-types",
        action="store_true",
        help="List available skin types and exit.",
    )
    parser.add_argument(
        "--api-key",
        help="API key for API-Ninjas (required for API mode).",
    )
    parser.add_argument(
        "--animal-name",
        help="Animal name to search for in API (if not provided, will prompt user).",
    )
    parser.add_argument(
        "--use-json",
        action="store_true",
        help="Use JSON file instead of API for data.",
    )
    return parser.parse_args(argv)


def main():
    """Generate the final HTML page by combining animal data with the template."""
    args = parse_args(sys.argv[1:])

    try:
        template_path = Path(args.template)

        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")

        # Get animal name from user input or command line argument
        if args.animal_name:
            animal_name = args.animal_name
        else:
            animal_name = input("Enter a name of an animal: ").strip()
            if not animal_name:
                raise ValueError("Animal name cannot be empty")

        # Use API by default, fall back to JSON file if --use-json flag is provided
        if not args.use_json:
            if not args.api_key:
                raise ValueError(
                    "API key is required. Please provide it using --api-key"
                )
            print(f"Fetching animal data for '{animal_name}' from API...")
            animal_data = fetch_animals_from_api(animal_name, args.api_key)
            print(f"Found {len(animal_data)} animals")

            # Handle case when no animals are found
            if not animal_data:
                print(
                    f"No animals found for '{animal_name}'. Generating error message..."
                )
                # Generate HTML with error message instead of animal data
                error_html = create_error_message(animal_name)
                template = load_text(str(template_path))
                html = template.replace("__REPLACE_ANIMALS_INFO__", error_html)

                output_path = Path(args.output)
                save_data(str(output_path), html)
                print(
                    f"Website was successfully generated to the file {output_path.name}."
                )
                return
        else:
            data_path = Path(args.data)
            if not data_path.exists():
                raise FileNotFoundError(f"Data file not found: {data_path}")
            animal_data = load_data(str(data_path))

        if args.list_skin_types:
            skin_types = list_skin_types(animal_data)
            if not skin_types:
                print("No skin type data found.")
                return
            print("Available skin types:")
            for index, skin_type in enumerate(skin_types, start=1):
                print(f"{index}. {skin_type}")
            return

        selected_skin_type = args.skin_type

        # Interactive prompt if no CLI skin type provided
        if selected_skin_type is None:
            skin_types = list_skin_types(animal_data)
            if skin_types:
                print("Available skin types:")
                for index, skin_type in enumerate(skin_types, start=1):
                    print(f"{index}. {skin_type}")
                selected_skin_type = prompt_skin_type(skin_types)
            else:
                selected_skin_type = "All"

        html = generate_html(
            data=animal_data,
            template_path=str(template_path),
            skin_type=selected_skin_type,
        )

        output_path = Path(args.output)
        save_data(str(output_path), html)
        print(f"Website was successfully generated to the file {output_path.name}.")
    except FileNotFoundError as exc:
        print(str(exc))
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"Failed to parse JSON: {exc}")
        sys.exit(1)
    except ValueError as exc:
        print(str(exc))
        sys.exit(2)
    except requests.RequestException as exc:
        print(f"API request failed: {exc}")
        sys.exit(3)


if __name__ == "__main__":
    main()
