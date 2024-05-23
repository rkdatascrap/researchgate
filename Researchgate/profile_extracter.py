from bs4 import BeautifulSoup
import pandas as pd
import logging
from functions.readpage import fun as rd
from functions.scrapper import scrapper as sc
import tkinter as tk
from tkinter import messagebox
import datetime

logging.basicConfig(filename="logger\/profilepage_extractor"+str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))+".log", level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info("Start of the automation")



def submit_action():
    #Get user input from the UI
    urls = entry1.get()
    url_list = urls.split(',')
    final_df = pd.DataFrame()
    columns=[("ProfileName","OrgName","Title","PublicationType","AuthorName","AuthorOrder","DatePublished","Journal","JournalCitations","Abstract","URL")]
    first_df=pd.DataFrame(columns)
    final_df = pd.concat([final_df, first_df], ignore_index=True)
    for url in url_list:
        print(url)
        if url.startswith("https://") and "profile" in url:
            logging.info("Input verified as Profile URL")
            noOfYears = year_var.get()
            #Start reading the page
            soup=rd(url)
            #start scrapping
            soup = BeautifulSoup(soup, 'html.parser')
            #creating output xls file
            new_df = pd.DataFrame(sc(soup,noOfYears))
            final_df = pd.concat([final_df, new_df], ignore_index=True)    
        else:
            logging.info("Input verification shows its not a proper URL")
            messagebox.showinfo("Failure", "Please provide correct URL")
    final_df.to_excel("output\/profileextracted_"+str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))+".xlsx", index=False, header=None)
    logging.info("Scrapped data successfully exported to output.xlsx")    
    messagebox.showinfo("Success", "Profile extraction completed, check output folder")

#main window
root = tk.Tk()
root.title("Researchgate Profile Data extractor")
#window size
root.geometry("400x150")

# first input label
label1 = tk.Label(root, text="Enter the Profile URL: ")
label1.grid(row=0, column=0, padx=5, pady=5)
entry1 = tk.Entry(root)
entry1.grid(row=0, column=1, padx=5, pady=5)

# Generate list of last 25 years
current_year = datetime.datetime.now().year
years = [str(year) for year in range(current_year, current_year - 25, -1)]

#second input label
label2 = tk.Label(root, text="Get Data from Current year to ")
label2.grid(row=1, column=0, padx=5, pady=5)
year_var = tk.StringVar(root)
year_var.set(years[10])  # defaulted value to 10 year data
year_menu = tk.OptionMenu(root, year_var, *years)
year_menu.grid(row=1, column=1, padx=5, pady=5)

# Create and place the submit button
submit_button = tk.Button(root, text="Submit", command=submit_action)
submit_button.grid(row=2, columnspan=2, pady=20)


# Run the Tkinter event loop
root.mainloop()