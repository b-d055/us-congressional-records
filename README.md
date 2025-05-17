# US Congressional Records

## Overview

This project provides a tool to efficiently download entire volumes of US Congressional Records from the congress.gov API. The records are fetched, compiled, and saved as text files for easy access and analysis.

## Usage

To use the `get_congressional_record.py` script, follow the steps below:

1. Ensure you have the required dependencies installed. You can install them using:
    ```sh
    pip install -r requirements.txt
    ```

2. Run the script with the required arguments:
    ```sh
    python get_congressional_record.py <volume> <api_key> [--force-override]
    ```

    - `<volume>`: The volume number of the Congressional Record.
    - `<api_key>`: Your API key for accessing congress.gov.
    - `--force-override` (optional): Use this flag to force override existing record files.

### Example

To fetch and compile articles for volume 165 with your API key:

```sh
python get_congressional_record.py 165 your_api_key_here
```

To force override existing files:

```sh
python get_congressional_record.py 165 your_api_key_here --force-override
```

### Notes

- There are rate limits on the congress.gov API endpoint. The script includes automatic retry logic with exponential backoff.
- Downloading an entire volume may take considerable time depending on the number of issues and articles.
- The script uses concurrent execution to speed up downloads where possible.
- Articles are saved as separate text files in directories organized by volume and issue number.

