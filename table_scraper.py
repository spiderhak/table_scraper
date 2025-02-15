import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import ttk, messagebox

class TableScraperUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Table Scraper")
        self.root.geometry("600x400")
        
        # Create and set up the UI elements
        self.setup_ui()
        
    def setup_ui(self):
        # URL input
        url_frame = ttk.LabelFrame(self.root, text="URL Settings", padding="10")
        url_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(url_frame, text="Website URL:").pack(anchor="w")
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(fill="x", pady=5)
        
        # Table class input
        ttk.Label(url_frame, text="Table Class (optional):").pack(anchor="w")
        self.table_class_entry = ttk.Entry(url_frame, width=50)
        self.table_class_entry.pack(fill="x", pady=5)
        
        # Output file input
        output_frame = ttk.LabelFrame(self.root, text="Output Settings", padding="10")
        output_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(output_frame, text="Output CSV filename:").pack(anchor="w")
        self.output_entry = ttk.Entry(output_frame, width=50)
        self.output_entry.pack(fill="x", pady=5)
        self.output_entry.insert(0, "output.csv")
        
        # Scrape button
        ttk.Button(self.root, text="Scrape Table", command=self.scrape_table).pack(pady=10)
        
        # Status text
        self.status_text = tk.Text(self.root, height=10, width=50)
        self.status_text.pack(padx=10, pady=5)
        
    def scrape_table(self):
        url = self.url_entry.get().strip()
        table_class = self.table_class_entry.get().strip()
        output_file = self.output_entry.get().strip()
        
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        try:
            # Send HTTP request
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find table
            if table_class:
                table = soup.find('table', class_=table_class)
            else:
                table = soup.find('table')
                
            if not table:
                raise Exception("No table found on the webpage")
                
            # Extract headers
            headers = []
            for th in table.find_all('th'):
                headers.append(th.text.strip())
                
            if not headers and table.find('tr'):
                # If no headers found, use first row as headers
                headers = [td.text.strip() for td in table.find('tr').find_all('td')]
                
            # Extract rows
            rows = []
            for tr in table.find_all('tr')[1:]:  # Skip header row
                row = [td.text.strip() for td in tr.find_all('td')]
                if row:  # Only append non-empty rows
                    rows.append(row)
                    
            # Write to CSV
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
                
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"Successfully scraped {len(rows)} rows to {output_file}")
            
        except Exception as e:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(tk.END, f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = TableScraperUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
