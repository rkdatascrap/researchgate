from bs4 import BeautifulSoup
import pandas as pd
import logging
from functions.readpage import fun as rd
from functions.scrapper import search_scrapper as ssc
import tkinter as tk
from tkinter import messagebox
import datetime

logging.basicConfig(filename="logger\/searchpage_extractor"+str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))+".log", level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info("Start of the automation")



def submit_action():
    #Get user input from the UI
    urls = entry1.get()
    url_list = urls.split(',')
    final_df = pd.DataFrame()
    columns=[("SearchKey","Title","PublicationType","AuthorName","AuthorOrder","DatePublished","Journal","JournalCitations","Abstract","URL")]
    first_df=pd.DataFrame(columns)
    final_df = pd.concat([final_df, first_df], ignore_index=True)
    filename="output\/searchpage_"+str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))+".xlsx"
    #final_df.to_excel(filename, index=False,header=False)
    for url in url_list:
        if url:
            logging.info("Input verified for search string")
            noOfYears = year_var.get()
            #make the search url
            for i in range(1,10):
                url=url.strip()
                searchUrl=f"https://www.researchgate.net/search/publication?q={url}&page={i}"
                #Start reading the page
                soup=rd(searchUrl)
                #start scrapping.
                soup = BeautifulSoup(soup, 'html.parser')
                new_df=pd.DataFrame(ssc(soup,noOfYears,url))
                #writer=pd.ExcelWriter(filename, engine='openpyxl',mode='a',if_sheet_exists="overlay")
                #new_df.to_excel(writer,index=False,header=False)
                #writer.save()
                final_df = pd.concat([final_df, new_df], ignore_index=True)
            #creating output xls file     
        else:
            logging.info("Input verification failed")
            messagebox.showinfo("Failure", "Please provide a alpha numeric word")
    final_df.to_excel(filename, index=False,header=False)
    logging.info("Scrapped data successfully exported to output.xlsx")   
    messagebox.showinfo("Success", "Profile extraction completed, check output folder")

#main window
root = tk.Tk()
root.title("Researchgate Search Data extractor")
#window size
root.geometry("400x150")

# first input label
label1 = tk.Label(root, text="Enter the Search Key word: ")
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