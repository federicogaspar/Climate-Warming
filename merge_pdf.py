#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 14:08:33 2021

@author: karina
"""


import os
from PyPDF2 import PdfFileMerger

def merge_pdf(foldername, foldername_end, folder_location=''):
        
    """
    Given a folder with city folders inside it, merge the pdfs that are inside 
    each city folder into one new pdf file and name them according to the city. 
    Saved all files inside the folder named 'foldername_end'.
    
    Args:
        foldername: Name of the folder where the cities folders are located (str)
        foldername_end: Name of the folder where the merge file will be saved (str).
        folder_location: directory where 'foldername' is located. By default 
        it takes the current working directory (str).        
        
    Retunrs:
        None.
     
    """
    
    #Create necessary directories.
    if not folder_location:
        cwd = os.getcwd()  # cwd is the place where the folder calendar_plots is.
    else:
        cwd = folder_location
    directory = os.path.join(cwd, foldername)
    dir_end = os.path.join(cwd, foldername_end)
    
    #Create the destination folder if it does not exist
    if not os.path.isdir(dir_end):
        os.mkdir(dir_end)
    
    #Create a dictionary with cities as keys and a list of pdfs as values
    pdfs = {}
    for root, dirs, files in os.walk(directory):
        if files:
            name = files[0][:-8]
            pdfs[name] = sorted(files)
    
    #Merge pdf from each dity and locate them in the folder 'calendar_plots_unified'
    for key in pdfs:
        os.chdir(os.path.join(directory, key)) 
        merger = PdfFileMerger()
        for file in pdfs[key]:
            merger.append(file)
        filename = key + '.pdf'
        dir_file = os.path.join(dir_end, filename)
        merger.write(dir_file)
        merger.close()

if __name__ == '__main__':
    foldername = 'calendar_plots'
    foldername_end = 'calendar_plots_unified'
    merge_pdf(foldername,  foldername_end)