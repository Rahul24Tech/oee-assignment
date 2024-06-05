# OEE Calculation Django Application

## Overview

This Django application is designed to calculate Overall Equipment Effectiveness (OEE) for machines based on production logs stored in a SQLite database. It provides a REST API to retrieve OEE data for machines and allows filtering by date ranges.

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd <repository-directory>

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt

3. **Apply migrations:**
   ```sh
   python manage.py migrate

4. **Run the server:**
   ```sh
   python manage.py runserver

5. **Access the OEE API:**
   ```sh
   /api/oee/: Retrieves OEE data for all machines.
    /api/oee_by_date/: Retrieves OEE data for machines within a specified date range

## Testing

**Run the tests using the following command:**
 
  python manage.py test

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
