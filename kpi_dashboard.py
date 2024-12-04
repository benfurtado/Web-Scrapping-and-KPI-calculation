import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF

# Loading the sales data from CSV
def load_data(file_path):
    return pd.read_csv(file_path)

# Calculates total sales per category
def calculate_total_sales(data):

    data['Year'] = pd.to_datetime(data['Date']).dt.year
    # Groups by Year and Category
    grouped = data.groupby(['Year', 'Category'])

    total_sales = grouped['TotalSales'].sum()
    print(total_sales)   

    return  total_sales

# Calculates Average Order Value (AOV) per category
def calculate_aov(data):
    data['Year'] = pd.to_datetime(data['Date']).dt.year
    # Groups by Year and Category
    grouped = data.groupby(['Year', 'Category'])

    # Calculates AOV: TotalSales sum divided by ProductID count
    aov = grouped['TotalSales'].sum() / grouped['ProductID'].count()
    
    print(aov)  # Debug: Print the AOV for each category
    return aov

# plotting the graphs for Total Sales and AOV
def plot_kpis(total_sales, aov):
    # Plot Total Sales per Category
    plt.figure(figsize=(10, 6))
    total_sales.plot(kind='bar', color='skyblue')
    plt.title('Total Sales per Category')
    plt.xlabel('Category')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('total_sales_per_category.png')
    plt.close()

    # Plot AOV per Category
    plt.figure(figsize=(10, 6))
    aov.plot(kind='bar', color='lightgreen')
    plt.title('Average Order Value (AOV) per Category')
    plt.xlabel('Category')
    plt.ylabel('Average Order Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('aov_per_category.png')
    plt.close()

# Save KPI Data to CSV
def save_kpis_to_csv(total_sales, aov, filename="kpi_data.csv"):
    kpi_data = pd.DataFrame({'TotalSales': total_sales, 'AOV': aov})
    kpi_data.to_csv(filename, index=True)
    print(f"KPI data saved to {filename}")

# Generate PDF Report and also saving the raw data in the pdf
def generate_pdf_report(total_sales, aov):
    current_date = datetime.now().strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(200, 10, txt="KPI Dashboard Report", ln=True, align='C')

    # Total Sales per Category (Chart + Data)
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(200, 10, txt="Total Sales per Category", ln=True)
    pdf.image('total_sales_per_category.png', x=10, y=30, w=180)
    pdf.ln(120)  # Adjust for image height
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Raw Data:", ln=True)
    for category, value in total_sales.items():
        pdf.cell(200, 10, txt=f"{category}: {value}", ln=True)

    
    pdf.add_page()

    # AOV per Category (Chart + Data)
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(200, 10, txt="Average Order Value (AOV) per Category", ln=True)
    pdf.image('aov_per_category.png', x=10, y=30, w=180)
    pdf.ln(120)  # Adjust for image height
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Raw Data:", ln=True)
    for category, value in aov.items():
        pdf.cell(200, 10, txt=f"{category}: {value:.2f}", ln=True)

    # Save the PDF
    pdf.output(f"kpi_dashboard-{current_date}.pdf") #added current date to prevent overwritingof daily save file
    print(f"PDF report generated as 'kpi_dashboard-{current_date}.pdf'")



# Main function to automate the dashboard creation
def main():
    # Load the data
    try:
        data = load_data("./Sales Data_1.csv")
    except Exception as e:
        print("Error: Could not load the data.")

    # Calculate KPIs
    total_sales = calculate_total_sales(data)
    aov = calculate_aov(data) 

    # Visualize KPIs
    plot_kpis(total_sales, aov)

    # Save KPI Data to CSV
    save_kpis_to_csv(total_sales, aov)

    # Generate PDF Report
    generate_pdf_report(total_sales, aov)

if __name__ == "__main__":
    main()
