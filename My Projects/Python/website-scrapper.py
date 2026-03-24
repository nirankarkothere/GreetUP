import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from urllib.parse import urlparse
import threading
import time
from datetime import datetime
import os

class WebScraper:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper Tool")
        self.root.geometry("900x700")
        self.root.configure(bg='#2C3E50')
        
        # Scraping variables
        self.scraped_data = []
        self.current_url = ""
        self.is_scraping = False
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        ]
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#34495E', height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🕷️ WEB SCRAPER TOOL 🕷️",
            font=('Arial', 24, 'bold'),
            bg='#34495E',
            fg='#F1C40F'
        )
        title_label.pack(expand=True)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#2C3E50')
        main_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # URL Input Section
        url_frame = tk.LabelFrame(
            main_container,
            text="🌐 Target URL",
            font=('Arial', 12, 'bold'),
            bg='#34495E',
            fg='#ECF0F1',
            bd=2,
            relief='groove'
        )
        url_frame.pack(fill='x', pady=(0, 20))
        
        # URL Entry
        url_input_frame = tk.Frame(url_frame, bg='#34495E')
        url_input_frame.pack(fill='x', padx=10, pady=10)
        
        self.url_entry = tk.Entry(
            url_input_frame,
            font=('Arial', 12),
            bg='#ECF0F1',
            fg='#2C3E50',
            bd=2,
            relief='sunken'
        )
        self.url_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.url_entry.insert(0, "https://books.toscrape.com/")  # Example URL
        
        # Scrape Button
        self.scrape_btn = tk.Button(
            url_input_frame,
            text="🚀 Start Scraping",
            font=('Arial', 12, 'bold'),
            bg='#27AE60',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.start_scraping
        )
        self.scrape_btn.pack(side='right')
        
        # Preset Websites Frame
        preset_frame = tk.Frame(url_frame, bg='#34495E')
        preset_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            preset_frame,
            text="Quick Select:",
            font=('Arial', 10),
            bg='#34495E',
            fg='#ECF0F1'
        ).pack(side='left', padx=(0, 10))
        
        presets = [
            ("Books", "https://books.toscrape.com/"),
            ("Quotes", "https://quotes.toscrape.com/"),
            ("Fake Python Jobs", "http://pythonjobs.github.io/"),
            ("News", "https://news.ycombinator.com/")
        ]
        
        for name, url in presets:
            btn = tk.Button(
                preset_frame,
                text=name,
                font=('Arial', 9),
                bg='#3498DB',
                fg='white',
                bd=0,
                padx=10,
                cursor='hand2',
                command=lambda u=url: self.set_url(u)
            )
            btn.pack(side='left', padx=5)
        
        # Configuration Section
        config_frame = tk.LabelFrame(
            main_container,
            text="⚙️ Scraping Configuration",
            font=('Arial', 12, 'bold'),
            bg='#34495E',
            fg='#ECF0F1',
            bd=2,
            relief='groove'
        )
        config_frame.pack(fill='x', pady=(0, 20))
        
        # Config options
        config_inner = tk.Frame(config_frame, bg='#34495E')
        config_inner.pack(fill='x', padx=10, pady=10)
        
        # Scraping Type
        tk.Label(
            config_inner,
            text="Scrape Type:",
            font=('Arial', 10),
            bg='#34495E',
            fg='#ECF0F1'
        ).grid(row=0, column=0, sticky='w', padx=(0, 20), pady=5)
        
        self.scrape_type = tk.StringVar(value="tables")
        types = [("Tables", "tables"), ("Lists", "lists"), ("Paragraphs", "paragraphs"), 
                 ("Links", "links"), ("Images", "images"), ("Custom", "custom")]
        
        for i, (text, value) in enumerate(types):
            rb = tk.Radiobutton(
                config_inner,
                text=text,
                value=value,
                variable=self.scrape_type,
                bg='#34495E',
                fg='#ECF0F1',
                selectcolor='#34495E',
                activebackground='#34495E'
            )
            rb.grid(row=i//3, column=i%3+1, sticky='w', padx=10, pady=2)
        
        # CSS Selector (for custom scraping)
        tk.Label(
            config_inner,
            text="CSS Selector:",
            font=('Arial', 10),
            bg='#34495E',
            fg='#ECF0F1'
        ).grid(row=2, column=0, sticky='w', padx=(0, 20), pady=5)
        
        self.selector_entry = tk.Entry(
            config_inner,
            font=('Arial', 10),
            bg='#ECF0F1',
            fg='#2C3E50',
            width=30
        )
        self.selector_entry.grid(row=2, column=1, columnspan=2, sticky='w', pady=5)
        self.selector_entry.insert(0, ".product")  # Example selector
        
        # Progress Section
        progress_frame = tk.Frame(main_container, bg='#2C3E50')
        progress_frame.pack(fill='x', pady=(0, 10))
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to scrape...",
            font=('Arial', 10),
            bg='#2C3E50',
            fg='#ECF0F1'
        )
        self.progress_label.pack(side='left')
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=200
        )
        self.progress_bar.pack(side='right')
        
        # Results Section (Treeview)
        results_frame = tk.LabelFrame(
            main_container,
            text="📊 Scraped Data",
            font=('Arial', 12, 'bold'),
            bg='#34495E',
            fg='#ECF0F1',
            bd=2,
            relief='groove'
        )
        results_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Treeview with scrollbars
        tree_frame = tk.Frame(results_frame, bg='#34495E')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Vertical scrollbar
        v_scrollbar = tk.Scrollbar(tree_frame)
        v_scrollbar.pack(side='right', fill='y')
        
        # Horizontal scrollbar
        h_scrollbar = tk.Scrollbar(tree_frame, orient='horizontal')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            show='headings'
        )
        
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        self.tree.pack(fill='both', expand=True)
        
        # Export Buttons Frame
        export_frame = tk.Frame(main_container, bg='#2C3E50')
        export_frame.pack(fill='x')
        
        # Export buttons
        buttons = [
            ("📥 Export to CSV", self.export_csv, '#27AE60'),
            ("📊 Export to Excel", self.export_excel, '#2980B9'),
            ("📋 Copy to Clipboard", self.copy_to_clipboard, '#F39C12'),
            ("🔄 Clear Data", self.clear_data, '#E74C3C')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                export_frame,
                text=text,
                font=('Arial', 11, 'bold'),
                bg=color,
                fg='white',
                bd=0,
                padx=20,
                pady=8,
                cursor='hand2',
                command=command
            )
            btn.pack(side='left', padx=5, expand=True, fill='x')
            
            # Hover effect
            btn.bind('<Enter>', lambda e, b=btn, c=color: b.configure(bg=self.darken_color(c)))
            btn.bind('<Leave>', lambda e, b=btn, c=color: b.configure(bg=c))
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            font=('Arial', 9),
            bg='#34495E',
            fg='#ECF0F1',
            anchor='w'
        )
        self.status_bar.pack(side='bottom', fill='x')
    
    def darken_color(self, color):
        """Darken a color for hover effect"""
        if color.startswith('#'):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            
            r = max(0, r - 20)
            g = max(0, g - 20)
            b = max(0, b - 20)
            
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def set_url(self, url):
        """Set URL in entry field"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
    
    def start_scraping(self):
        """Start the scraping process in a separate thread"""
        if self.is_scraping:
            messagebox.showwarning("In Progress", "Scraping is already in progress!")
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL to scrape!")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
        
        self.current_url = url
        self.is_scraping = True
        
        # Disable scrape button and start progress
        self.scrape_btn.config(state='disabled', bg='#7F8C8D')
        self.progress_bar.start(10)
        self.progress_label.config(text="🔄 Scraping in progress...")
        self.status_bar.config(text=f"Scraping: {url}")
        
        # Start scraping thread
        thread = threading.Thread(target=self.scrape_website)
        thread.daemon = True
        thread.start()
    
    def scrape_website(self):
        """Perform the actual scraping"""
        try:
            # Rotate user agent
            headers = {
                'User-Agent': self.user_agents[hash(self.current_url) % len(self.user_agents)]
            }
            
            # Make request
            response = requests.get(self.current_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Scrape based on type
            scrape_type = self.scrape_type.get()
            
            if scrape_type == "tables":
                data = self.scrape_tables(soup)
            elif scrape_type == "lists":
                data = self.scrape_lists(soup)
            elif scrape_type == "paragraphs":
                data = self.scrape_paragraphs(soup)
            elif scrape_type == "links":
                data = self.scrape_links(soup)
            elif scrape_type == "images":
                data = self.scrape_images(soup)
            else:  # custom
                selector = self.selector_entry.get().strip()
                data = self.scrape_custom(soup, selector)
            
            # Update UI with results
            self.root.after(0, self.display_results, data)
            
        except requests.RequestException as e:
            self.root.after(0, self.show_error, f"Network Error: {str(e)}")
        except Exception as e:
            self.root.after(0, self.show_error, f"Scraping Error: {str(e)}")
        finally:
            self.root.after(0, self.scraping_complete)
    
    def scrape_tables(self, soup):
        """Scrape all tables from the page"""
        data = []
        tables = soup.find_all('table')
        
        for i, table in enumerate(tables, 1):
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                cell_text = [cell.get_text(strip=True) for cell in cells]
                if cell_text:
                    data.append({
                        'Table': f'Table {i}',
                        'Row': len(data) + 1,
                        'Content': ' | '.join(cell_text)
                    })
        
        return data
    
    def scrape_lists(self, soup):
        """Scrape all lists from the page"""
        data = []
        list_types = ['ul', 'ol', 'dl']
        
        for list_type in list_types:
            lists = soup.find_all(list_type)
            for i, lst in enumerate(lists, 1):
                items = lst.find_all('li') if list_type != 'dl' else lst.find_all(['dt', 'dd'])
                for j, item in enumerate(items, 1):
                    data.append({
                        'List Type': list_type.upper(),
                        'List Number': i,
                        'Item Number': j,
                        'Content': item.get_text(strip=True)
                    })
        
        return data
    
    def scrape_paragraphs(self, soup):
        """Scrape all paragraphs from the page"""
        data = []
        paragraphs = soup.find_all('p')
        
        for i, p in enumerate(paragraphs, 1):
            text = p.get_text(strip=True)
            if text:  # Only add non-empty paragraphs
                data.append({
                    'Paragraph #': i,
                    'Content': text,
                    'Length': len(text)
                })
        
        return data
    
    def scrape_links(self, soup):
        """Scrape all links from the page"""
        data = []
        links = soup.find_all('a', href=True)
        
        for i, link in enumerate(links, 1):
            href = link['href']
            text = link.get_text(strip=True)
            
            # Convert relative URLs to absolute
            if not href.startswith(('http://', 'https://')):
                href = urlparse(self.current_url)._replace(path=href).geturl()
            
            data.append({
                'Link #': i,
                'Text': text if text else '[No Text]',
                'URL': href,
                'Type': 'External' if href.startswith('http') else 'Internal'
            })
        
        return data
    
    def scrape_images(self, soup):
        """Scrape all images from the page"""
        data = []
        images = soup.find_all('img')
        
        for i, img in enumerate(images, 1):
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            # Convert relative URLs to absolute
            if src and not src.startswith(('http://', 'https://')):
                src = urlparse(self.current_url)._replace(path=src).geturl()
            
            data.append({
                'Image #': i,
                'Alt Text': alt if alt else '[No Alt]',
                'Source': src if src else '[No Source]',
                'Width': img.get('width', 'N/A'),
                'Height': img.get('height', 'N/A')
            })
        
        return data
    
    def scrape_custom(self, soup, selector):
        """Scrape using custom CSS selector"""
        data = []
        elements = soup.select(selector)
        
        for i, element in enumerate(elements, 1):
            data.append({
                'Element #': i,
                'HTML': str(element)[:100] + '...' if len(str(element)) > 100 else str(element),
                'Text': element.get_text(strip=True),
                'Class': ' '.join(element.get('class', [])),
                'ID': element.get('id', 'N/A')
            })
        
        return data
    
    def display_results(self, data):
        """Display scraped data in treeview"""
        if not data:
            messagebox.showinfo("No Data", "No data found on the page with current settings!")
            return
        
        self.scraped_data = data
        
        # Clear existing treeview
        self.tree.delete(*self.tree.get_children())
        
        # Configure columns based on data keys
        if data:
            columns = list(data[0].keys())
            self.tree['columns'] = columns
            
            # Configure columns
            for col in columns:
                self.tree.heading(col, text=col, anchor='w')
                self.tree.column(col, width=150, anchor='w')
            
            # Insert data
            for i, row in enumerate(data):
                values = [row.get(col, '') for col in columns]
                self.tree.insert('', 'end', values=values, tags=('row', i))
        
        self.progress_label.config(text=f"✅ Scraped {len(data)} items successfully!")
        self.status_bar.config(text=f"Last scrape: {datetime.now().strftime('%H:%M:%S')}")
    
    def scraping_complete(self):
        """Handle scraping completion"""
        self.is_scraping = False
        self.scrape_btn.config(state='normal', bg='#27AE60')
        self.progress_bar.stop()
    
    def show_error(self, error_msg):
        """Show error message"""
        messagebox.showerror("Scraping Error", error_msg)
        self.progress_label.config(text="❌ Scraping failed!")
        self.status_bar.config(text=f"Error: {error_msg}")
    
    def export_csv(self):
        """Export data to CSV file"""
        if not self.scraped_data:
            messagebox.showwarning("No Data", "No data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if filename:
            try:
                keys = self.scraped_data[0].keys()
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(self.scraped_data)
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
                self.status_bar.config(text=f"Exported to: {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
    
    def export_excel(self):
        """Export data to Excel file"""
        if not self.scraped_data:
            messagebox.showwarning("No Data", "No data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=f"scraped_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        if filename:
            try:
                df = pd.DataFrame(self.scraped_data)
                df.to_excel(filename, index=False)
                
                messagebox.showinfo("Success", f"Data exported to {filename}")
                self.status_bar.config(text=f"Exported to: {filename}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
    
    def copy_to_clipboard(self):
        """Copy data to clipboard"""
        if not self.scraped_data:
            messagebox.showwarning("No Data", "No data to copy!")
            return
        
        try:
            # Convert to CSV format
            keys = self.scraped_data[0].keys()
            output = ','.join(keys) + '\n'
            for row in self.scraped_data:
                output += ','.join(str(row.get(k, '')) for k in keys) + '\n'
            
            self.root.clipboard_clear()
            self.root.clipboard_append(output)
            
            messagebox.showinfo("Success", "Data copied to clipboard!")
            self.status_bar.config(text=f"Copied {len(self.scraped_data)} rows to clipboard")
        except Exception as e:
            messagebox.showerror("Copy Error", str(e))
    
    def clear_data(self):
        """Clear all scraped data"""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all data?"):
            self.scraped_data = []
            self.tree.delete(*self.tree.get_children())
            self.progress_label.config(text="Data cleared")
            self.status_bar.config(text="Ready")

class AdvancedWebScraper:
    def __init__(self):
        self.root = tk.Tk()
        self.app = WebScraper(self.root)
        self.root.mainloop()

if __name__ == "__main__":
    # Install required packages if not present
    try:
        import requests
        from bs4 import BeautifulSoup
        import pandas as pd
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please install: pip install requests beautifulsoup4 pandas")
        exit(1)
    
    # Run the application
    scraper = AdvancedWebScraper()