This script creates a user-friendly GUI application that allows you to:
Enter a URL of the webpage containing the table
Optionally specify a table class if there are multiple tables
Specify the output CSV filename
Scrape the table data and save it to a CSV file
Features:
Handles tables with or without <tbody> tags
Supports tables with class attributes
Automatically detects table headers (th tags) or uses first row as headers
Shows status updates and error messages
Saves the scraped data in CSV format with UTF-8 encoding
To use the script:
Run the script
Enter the URL of the webpage containing the table
If the table has a specific class, enter it in the "Table Class" field
Enter the desired output filename (defaults to "output.csv")
Click "Scrape Table" to start the scraping process
Required Python packages:
requests
beautifulsoup4
tkinter (usually comes with Python)
