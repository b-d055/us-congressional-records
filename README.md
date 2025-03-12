# US Congressional Records

## Motivation

This project aims to efficiently download entire volumes of US Congressional Records from the congress.gov API. The records are fetched, compiled, and saved as text files for easy access and analysis.

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

### Note

There are rate limits on the congress.gov API endpoint, hence the retries in the script. It may take a while to download an entire volume, especially if there are many issues and articles.

### Available Data

The 2024 volume (Volume 170) has already been pulled in its entirety and is available in the `congressional_records_170` directory.
