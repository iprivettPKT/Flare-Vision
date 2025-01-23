import pandas as pd
import os

def csv_to_filtered_searchable_html():
    """
    Converts a CSV file into a simplified, searchable HTML file with sections for each category.
    Handles rows without a category_name by assigning them to 'Uncategorized' and displays external_url and external_netloc as plain text.
    Asks the user for the file path and generates an output HTML file with a similar name.
    """

    # ASCII Banner
    print(r"""
   ███████╗██╗      █████╗ ██████╗ ███████╗    ██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗
   ██╔════╝██║     ██╔══██╗██╔══██╗██╔════╝    ██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║
   █████╗  ██║     ███████║██████╔╝█████╗      ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║
   ██╔══╝  ██║     ██╔══██║██╔══██╗██╔══╝      ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║
   ██║     ███████╗██║  ██║██║  ██║███████╗     ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║
   ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝      ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                                                                                            
    
    By: Isaac Privett
    This is a script to convert a Flare CSV export into a searchable HTML file. 
    It will ask for the path to the CSV file and then generate an HTML file with a similar name. 
    
    Instructions: export the full Flare CSV file from the Flare web app and run this script.
          """)

    try:
        # Prompt user for the input CSV file path
        input_csv = input("Enter the path to the Flare CSV file: ").strip()
        
        # Generate the output HTML file path
        output_html = os.path.splitext(input_csv)[0] + "_filtered_searchable.html"
        
        # Load the CSV file
        csv_data = pd.read_csv(input_csv, dtype=str)  # Ensure all data is read as strings
        
        # Define relevant columns for red team purposes
        relevant_columns = [
            "category_name",       # Grouping
            "credential_preview",  # Summary of leaked credentials
            "id",                  # Unique identifier
            "source_name",         # Source of the leak
            "browser_url",         # External net location (plain text)
            "title",               # Description of the leak
            "posted_at"            # Date when the data was posted
        ]
        
        # Filter the data for relevant columns
        filtered_data = csv_data[relevant_columns]
        
        # Replace NaN values with empty strings
        filtered_data = filtered_data.fillna("")
        
        # Assign a default category name for rows without one
        filtered_data["category_name"] = filtered_data["category_name"].replace("", "Uncategorized")
        
        # Start building the HTML content
        html_content = """
        <html>
        <head>
            <title>Filtered Flare Data</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1, h2 { color: #333; }
                table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f4f4f4; }
                .search-bar { margin-bottom: 20px; }
                .search-bar input { width: 100%; padding: 10px; font-size: 16px; }
            </style>
            <script>
                function searchTable() {
                    const input = document.getElementById('searchInput');
                    const filter = input.value.toLowerCase();
                    const tables = document.querySelectorAll('table');
                    
                    tables.forEach(table => {
                        const rows = table.getElementsByTagName('tr');
                        let hasVisibleRow = false;
                        
                        for (let i = 1; i < rows.length; i++) { // Skip the header row
                            const cells = rows[i].getElementsByTagName('td');
                            let rowVisible = false;
                            
                            for (let j = 0; j < cells.length; j++) {
                                if (cells[j].textContent.toLowerCase().includes(filter)) {
                                    rowVisible = true;
                                    break;
                                }
                            }
                            
                            rows[i].style.display = rowVisible ? '' : 'none';
                            if (rowVisible) hasVisibleRow = true;
                        }
                        
                        // Show/hide the table based on whether any rows are visible
                        table.style.display = hasVisibleRow ? '' : 'none';
                    });
                }
            </script>
        </head>
        <body>
            <h1>Filtered Flare Data Export</h1>
            <div class="search-bar">
                <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for data...">
            </div>
        """

        # Group the data by 'category_name' and create HTML sections for each
        grouped_data = filtered_data.groupby('category_name')
        for category, group in grouped_data:
            html_content += f"<h2>{category}</h2>"
            html_content += group.to_html(index=False, escape=False)

        # Close the HTML tags
        html_content += "</body></html>"

        # Save the HTML content to a file
        with open(output_html, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        
        print(f"Searchable HTML file created successfully: {output_html}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
csv_to_filtered_searchable_html()
