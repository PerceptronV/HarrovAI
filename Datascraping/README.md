# Using the dataloader

## Prerequisites

* Python >= 3.8

* Installed packages Selenium, BeautifulSoup, tqdm, keyboard 

* Downloaded compatible Chromium drivers

* Adobe Acrobat DC (_not Adobe Reader_) is set as your default PDF reader

* A registered account at the [Harrovian Archive](https://theharrovian.org)

## Downloading data

* Clone this repository

* Edit your search parameters in `SearchConfig.json`

    * To make the Chrome window invisible during the downloading process, add `"--headless""` under `ChromeOptions`.
      
        This is not recommended, however, because if the program stops due to a bug, the invisible Chrome window will still be running in the background and cannot be terminated.
      
        ```json
        "ChromeOptions":
        [
          "--headless"
        ]
        ```
    
    * Under `SearchParams` you will find a list of customisable search configurations, laid out under the following structure:
        ```json5
        "SearchParams":
        [
          {
            // Name of the search, used as an identifier
            "Name": "Gaffe", 
            
            // Whether the search has been performed and all the data downloaded already
            "Done": false, 
            "Selections":
            {
              "ddlYearFrom": "1990", // Use "--All--" to access all available years
              "ddlYearTo": "2020", // Use "--All--" to access all available years
              "ddlVolume": "--All Volumes--",
              "ddlIssue": "--All Issues--",
              "ddlJournal": "Harrovian", // Use "--All Journals--" to access all available journals
              "ddlArticleType": "--All Types--",
              "ddlCategory": "--All Categories --"
            },
            // Specify keywords to look for; can be left blank
            "SearchText": "Gaffe and Gown",
              
            // Where to look for the SearchText; use "Title" when in doubt
            "SearchScope": "Title", // Other valid scopes include: "Title", "Keywords", "BodyText", "Archivist", "Guest"
          
            // Path to save downloaded materials; if null, defaults to 'Data\{SearchName}' of current dir
            "SavePath": null
          }
        ]  
        ```

* Edit `load_all.py` to include the path to your Chromedriver
    
    ```python
    evoke('path_to\your\chromedriver.exe')
    ```

* Run `load_all.py`. A few points to note:

    * When your Chrome window pops up and lands at the login page, remember not to sign in on Chrome, but instead do so in your Python console.
    
    * The PDFs take a long time to download because the files are large and the Harrovian Archive server is slow
    
    * Once all the PDFs in a page have been downloaded, you will see Adobe Acrobat DC opening automatically, and converting all PDFs to text.
      
        At this point, it is best to leave your computer as it is to be controlled by the program, because little interference might be enough to mess up the process. Don't worry; this is not malware 😂!
  
* Typical searches involving downloading 100+ PDFs would need about an hour and a half to run (from start to finish).
