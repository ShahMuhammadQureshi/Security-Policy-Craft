import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import csv
from fpdf import FPDF

def perform_network_assessment(network_size, connected_devices, internet_usage, data_sensitivity):
    # Logic to collect network assessment data from user input
    assessment_result = f"Network Assessment\nNetwork Size: {network_size}\nConnected Devices: {connected_devices}\nInternet Usage: {internet_usage}\nData Sensitivity: {data_sensitivity}"
    messagebox.showinfo("Network Assessment", assessment_result)

def perform_risk_assessment(data_sensitivity, connected_devices, internet_usage, network_size):
    # Logic to analyze network assessment data
    risk_score = 0
    if "high" in data_sensitivity:
        risk_score += 10
    elif "medium" in data_sensitivity:
        risk_score += 5
    elif "low" in data_sensitivity:
        risk_score += 2
    
    if "home" in network_size:
        risk_score += 5
    elif "office" in network_size:
        risk_score += 10
    
    if "laptops" in connected_devices:
        risk_score += 7
    elif "desktops" in connected_devices:
        risk_score += 5
    elif "IoT devices" in connected_devices:
        risk_score += 3

    if "online transactions" in internet_usage:
        risk_score += 7
    elif "work" in internet_usage:
        risk_score += 3
    elif "entertainment" in internet_usage:
        risk_score += 2

    return risk_score

def generate_recommendations(risk_score):
    # Logic to suggest appropriate security controls based on risk profile
    recommendations = []
    if risk_score >= 15:
        recommendations.append("Enable two-factor authentication for all accounts")
    if risk_score >= 5:
        recommendations.append("Regularly update software and firmware")
    if risk_score >= 10:
        recommendations.append("Use a password manager to generate and store strong, unique passwords")
    return recommendations

def pick_recommendations(recommendations_csv, risk_score, network_size, connected_devices, internet_usage):
    selected_recommendations = []
    with open(recommendations_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row_risk_score = int(row['Risk Score'])

            if (row['Network Size'] == network_size and
                row['Connected Devices'] == connected_devices and
                row['Internet Usage'] == internet_usage and
                row_risk_score == risk_score):  
                selected_recommendations.append(row['Recommendation'])

    return selected_recommendations

def perform_network_assessment_ui():
    network_size = network_size_var.get()
    connected_devices = connected_devices_var.get()
    internet_usage = internet_usage_var.get()
    data_sensitivity = data_sensitivity_var.get()

    if network_size not in ["home", "office"]:
        messagebox.showerror("Error", "Invalid network size. Please enter 'home' or 'office'.")
        return

    if connected_devices not in ["laptops", "desktops", "IoT devices"]:
        messagebox.showerror("Error", "Invalid connected devices. Please enter 'laptops', 'desktops', or 'IoT devices'.")
        return

    if internet_usage not in ["work", "entertainment", "online transactions"]:
        messagebox.showerror("Error", "Invalid internet usage. Please enter 'work', 'entertainment', or 'online transactions'.")
        return
    
    if data_sensitivity not in ["low", "medium", "high"]:
        messagebox.showerror("Error", "Invalid data sensitivity. Please enter 'low', 'medium', or 'high'.")
        return
    
    perform_network_assessment(network_size, connected_devices, internet_usage, data_sensitivity)

def perform_risk_assessment_ui():
    data_sensitivity = data_sensitivity_var.get()
    if data_sensitivity not in ["low", "medium", "high"]:
        messagebox.showerror("Error", "Invalid data sensitivity. Please enter 'low', 'medium', or 'high'.")
        return

    risk_score = perform_risk_assessment(data_sensitivity, connected_devices_var.get(), internet_usage_var.get(), network_size_var.get())
    messagebox.showinfo("Risk Assessment", f"Risk Score: {risk_score}")


# Function to create PDF with recommendations
def create_pdf(general_recommendations, selected_recommendations):
    
    pdf = FPDF()
    pdf.add_page()

    # Set font for the title
    pdf.set_font("Arial", style='B', size=26)

    # Title
    pdf.cell(200, 10, txt="Policy Craft", ln=True, align='C')

    pdf.ln()
    # General Recommendations
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="\nGeneral Recommendations:", ln=True)
    pdf.set_font("Arial", size=12)
    for rec in general_recommendations:
        pdf.multi_cell(0, 10, txt="- " + rec)

    pdf.ln()
    # Specific Recommendations
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, txt="\nSpecific Recommendations:", ln=True)
    pdf.set_font("Arial", size=12)
    print(selected_recommendations)
    for rec in selected_recommendations:
        pdf.multi_cell(0, 10, txt=rec)

    pdf_output = "security_policies.pdf"
    pdf.output(pdf_output)

    print(f"PDF file '{pdf_output}' created successfully.")


def generate_pdf_on_click(general_recommendations, selected_recommendations):
    # Call the function to create PDF with recommendations
    create_pdf(general_recommendations, selected_recommendations)


def show_recommendations_ui():
    network_size = network_size_var.get()
    connected_devices = connected_devices_var.get()
    internet_usage = internet_usage_var.get()
    data_sensitivity = data_sensitivity_var.get()

    if network_size not in ["home", "office"]:
        messagebox.showerror("Error", "Invalid network size. Please enter 'home' or 'office'.")
        return

    if connected_devices not in ["laptops", "desktops", "IoT devices"]:
        messagebox.showerror("Error", "Invalid connected devices. Please enter 'laptops', 'desktops', or 'IoT devices'.")
        return

    if internet_usage not in ["work", "entertainment", "online transactions"]:
        messagebox.showerror("Error", "Invalid internet usage. Please enter 'work', 'entertainment', or 'online transactions'.")
        return

    if data_sensitivity not in ["low", "medium", "high"]:
        messagebox.showerror("Error", "Invalid data sensitivity. Please enter 'low', 'medium', or 'high'.")
        return

    recommendations_csv = 'recommendations.csv'
    risk_score = perform_risk_assessment(data_sensitivity, connected_devices, internet_usage, network_size)
    selected_recommendations = pick_recommendations(recommendations_csv, risk_score, network_size, connected_devices, internet_usage)

    general_recommendations = generate_recommendations(risk_score)
    recommendations_text = f"General Recommendations:\n{', '.join(general_recommendations)}\n\nSpecific Recommendations:\n{', '.join(selected_recommendations)}"
    messagebox.showinfo("Recommendations", recommendations_text)
    print(selected_recommendations)
    pdf_button = tk.Button(root, text="Generate PDF", command=lambda: generate_pdf_on_click(general_recommendations, selected_recommendations))
    pdf_button.grid(row=7, column=0, columnspan=2)





#-----------------------------------------------
# UI wala kaaam
root = tk.Tk()
root.title("Policy Craft")
# Set the size of the window
root.geometry("300x300")

# Create UI elements
network_size_label = tk.Label(root, text="Network Size: ")
network_size_label.grid(row=0, column=0)
network_size_var = tk.StringVar(root)
network_size_dropdown = tk.OptionMenu(root, network_size_var, "home", "office")
network_size_dropdown.grid(row=0, column=1)


connected_devices_label = tk.Label(root, text="Connected Devices: ")
connected_devices_label.grid(row=1, column=0)
connected_devices_var = tk.StringVar(root)
connected_devices_dropdown = tk.OptionMenu(root, connected_devices_var, "laptops", "desktops", "IoT devices")
connected_devices_dropdown.grid(row=1, column=1)

internet_usage_label = tk.Label(root, text="Internet Usage: ")
internet_usage_label.grid(row=2, column=0)
internet_usage_var = tk.StringVar(root)
internet_usage_dropdown = tk.OptionMenu(root, internet_usage_var, "work", "entertainment", "online transactions")
internet_usage_dropdown.grid(row=2, column=1)

data_sensitivity_label = tk.Label(root, text="Data sensitivity: ")
data_sensitivity_label.grid(row=3, column=0)
data_sensitivity_var = tk.StringVar(root)
data_sensitivity_dropdown = tk.OptionMenu(root, data_sensitivity_var, "low", "medium", "high")
data_sensitivity_dropdown.grid(row=3, column=1)

network_assessment_button = tk.Button(root, text="Show my network Info", command=perform_network_assessment_ui)
network_assessment_button.grid(row=4, column=0, columnspan=2)

risk_assessment_button = tk.Button(root, text="View Risk Score", command=perform_risk_assessment_ui)
risk_assessment_button.grid(row=5, column=0, columnspan=2)

recommendations_button = tk.Button(root, text="Get Recommendations", command=show_recommendations_ui)
recommendations_button.grid(row=6, column=0, columnspan=2)

# To Run the application
root.mainloop()
