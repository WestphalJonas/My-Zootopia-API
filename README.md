# My Zootopia API

A Python application that generates beautiful HTML websites displaying animal information. The project fetches animal data from the API-Ninjas API or local JSON files and creates interactive web pages with filtering capabilities.

## 🏗️ Architecture

This project follows a clean multi-file architecture with clear separation of concerns:

### Data Fetcher (`data_fetcher.py`)
- **Purpose**: Handles all data retrieval operations
- **Responsibilities**:
  - Fetch animal data from API-Ninjas API
  - Load animal data from local JSON files
  - Manage API authentication using environment variables
- **Key Function**: `fetch_data(animal_name, api_key=None, use_json=False)`

### Website Generator (`animals_web_generator.py`)
- **Purpose**: Generates HTML websites from animal data
- **Responsibilities**:
  - Create interactive HTML pages
  - Handle user input and command-line arguments
  - Filter animals by skin type
  - Generate error pages for missing data
- **Key Features**:
  - Interactive skin type filtering
  - Command-line interface
  - Template-based HTML generation

## 🚀 Features

- **Dual Data Sources**: Works with both API and local JSON data
- **Interactive Filtering**: Filter animals by skin type (Fur, Hair, Scales, etc.)
- **Environment Variables**: Secure API key management
- **Command-Line Interface**: Flexible usage options
- **Error Handling**: Graceful handling of missing data or API failures
- **Responsive Design**: Beautiful, modern HTML output

## 📋 Prerequisites

- Python 3.8+
- uv (for dependency management)
- API-Ninjas API key (for live data)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd My-Zootopia-API
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   API_KEY='your-api-ninjas-key-here'
   ```

## 🎯 Usage

### Basic Usage

**Generate website from API data**:
```bash
uv run python animals_web_generator.py --animal-name "fox"
```

**Generate website from JSON file**:
```bash
uv run python animals_web_generator.py --use-json --animal-name "fox"
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--animal-name` | Name of the animal to search for | Interactive prompt |
| `--use-json` | Use local JSON file instead of API | False |
| `--api-key` | Override API key from environment | Uses .env file |
| `--skin-type` | Filter by specific skin type | Interactive prompt |
| `--list-skin-types` | List available skin types and exit | False |
| `--template` | Path to HTML template | `animals_template.html` |
| `--data` | Path to JSON data file | `animals_data.json` |
| `--output` | Output HTML file path | `animals.html` |

### Examples

**List available skin types**:
```bash
uv run python animals_web_generator.py --use-json --list-skin-types
```

**Generate with specific skin type**:
```bash
uv run python animals_web_generator.py --animal-name "fox" --skin-type "Fur"
```

**Use custom template and output**:
```bash
uv run python animals_web_generator.py --animal-name "fox" --template "custom.html" --output "fox_animals.html"
```

## 🔧 Configuration

### Environment Variables

The application uses environment variables for configuration:

- **API_KEY**: Your API-Ninjas API key (required for API mode)

### File Structure

```
My-Zootopia-API/
├── animals_web_generator.py    # Main website generator
├── data_fetcher.py            # Data fetching module
├── animals_template.html      # HTML template
├── animals_data.json         # Sample animal data
├── .env                      # Environment variables (not tracked)
├── .gitignore               # Git ignore rules
├── pyproject.toml           # uv project configuration
└── README.md                # This file
```

## 🔒 Security

- **API Keys**: Stored in `.env` file (not tracked by Git)
- **Sensitive Data**: All sensitive information is excluded from version control
- **Environment Isolation**: Each environment can have its own configuration

## 🐛 Error Handling

The application handles various error scenarios:

- **Missing API Key**: Clear error message with setup instructions
- **API Failures**: Graceful fallback and error reporting
- **Missing Files**: File not found errors with helpful messages
- **Invalid Data**: Data validation and error reporting
- **No Results**: Custom error page when no animals are found

## 🧪 Testing

**Test with JSON data**:
```bash
uv run python animals_web_generator.py --use-json --animal-name "fox" --skin-type "All"
```

**Test API connectivity**:
```bash
uv run python animals_web_generator.py --animal-name "fox" --skin-type "All"
```

## 📝 Development

### Adding New Features

1. **Data Fetcher**: Add new data sources in `data_fetcher.py`
2. **Website Generator**: Add new features in `animals_web_generator.py`
3. **Templates**: Modify `animals_template.html` for UI changes

### Code Structure

- **Modular Design**: Clear separation between data and presentation
- **Type Hints**: Full type annotation for better code quality
- **Error Handling**: Comprehensive error handling throughout
- **Documentation**: Detailed docstrings for all functions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of a Masterschool course assignment.

## 🆘 Troubleshooting

**Common Issues**:

1. **API Key Error**: Ensure your API key is correctly set in `.env` file
2. **Module Not Found**: Run `uv sync` to install dependencies
3. **File Not Found**: Check that template and data files exist
4. **Permission Errors**: Ensure write permissions for output directory

**Getting Help**:
- Check the error messages for specific guidance
- Verify your `.env` file configuration
- Ensure all dependencies are installed with `uv sync`
