# -FCST-Replacer-Multi-Filter---Streamlit-App
This Streamlit application is designed to update forecast (FCST) values in one dataset by matching records from another dataset based on specific key fields. It provides a user-friendly interface for selective data replacement with multi-filter capabilities.

What It Does
Primary Function
The app replaces FCST values in File 1 (Base) with corresponding values from File 2 (Source) based on exact matches of four key fields:
LOC (Location)
ITEM (Item Code)
CHANNEL (Sales Channel)
FDATE (Forecast Date)

Key Features
Multi-Filter Selection: Choose specific locations and forecast dates to update
Exact Match Logic: Only updates records with perfect key field matches
Data Preservation: Only modifies FCST values, keeps all other data intact
Preview Functionality: Shows sample output before download
Error Handling: Validates file structure and required columns

File Format Requirements
Input Files
Both files must be pipe-delimited (|) CSV or TXT files with the following structure:
Required Columns
Both files must contain these exact column names:
LOC - Location identifier
ITEM - Item/product identifier
CHANNEL - Sales channel identifier
FDATE - Forecast date
FCST - Forecast value (to be updated)

File 1 (Base File)
Contains the dataset to be updated
Special format: Single column with pipe-delimited values per row
Header row with column names separated by |
Data rows with values separated by |

File 2 (Source File)
Contains the new forecast values
Standard pipe-delimited CSV format
**
REQUIREMENTS : pip install streamlit pandas**

Used as the source for replacement values
