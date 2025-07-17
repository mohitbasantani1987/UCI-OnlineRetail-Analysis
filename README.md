# UCI Online Retail Analysis

This project analyzes the [UCI Online Retail II dataset](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II), which contains transactional data for a UK-based online retailer between 01/12/2010 and 09/12/2011. The project provides a 3-level reporting pipeline to generate clean, insightful PDF reports with visualizations using Python.

## Features

- **Data Preprocessing:** Cleans and merges data from multiple years, removes invalid or missing entries, and performs feature engineering.
- **Multi-Level Analysis:**
  - **Level-1:** Basic data overview and facts.
  - **Level-2:** Adds feature engineering and generates key visualizations (top countries, monthly revenue, top products).
  - **Level-3:** Advanced analysis with additional plots (correlation matrix, boxplots, KDE curves, etc.).
- **Automated PDF Reporting:** Generates downloadable PDF reports with tables, facts, and embedded plots.
- **Console Web App:** Select analysis level and check reports.

## Project Structure

- `baseAnalysis.py`
- `main.py`
- `online_retail_II.xlsx`
- `requirements.txt`
- `assets/` (generated plots)
- `processor/`
  - `dataProcessor.py`
- `reporter/`
  - `reportGenerator.py`
- `static/` (generated PDF reports)

## Getting Started

### Prerequisites

- Python 3.8+
- [UCI Online Retail II dataset](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II) (place as `online_retail_II.xlsx` in the project root)

### Installation

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

2. Run the app:
    ```sh
    python run main.py
    ```

3. Select the desired analysis level and download the generated PDF report.

## File Descriptions

- **main.py:** Entry point; loads data, runs python app, and manages report generation.
- **baseAnalysis.py:** Abstract base class for analysis.
- **processor/dataProcessor.py:** Data cleaning, feature engineering, and plot generation.
- **reporter/reportGenerator.py:** PDF report creation with tables and images.
- **assets/:** Stores generated plot images.
- **static/:** Stores generated PDF reports.

## Author

Mohit Basantani

## License

This project is for educational purposes only and is not intended for commercial use.
