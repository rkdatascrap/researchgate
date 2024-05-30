from bs4 import BeautifulSoup
import time
from functions.readpage import fun as rd
import logging
from functions.re_functions import split_text_and_numbers as split
import re



def scrapper(soup,noOfYears):
    output=[]
    try:

        #Name
        #Name = soup.find('div', class_='nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-xxs nova-legacy-e-text--color-inherit')
        Name = soup.find('div', class_='nova-legacy-e-text--color-inherit')
        if Name:
            ProfileName = Name.get_text()
        else:
            ProfileName="NAME not found"

        #Org data
        Org=soup.find('span', class_='org')
        if Org:
            OrgName = Org.get_text()
        else:
            OrgName=" "
        #publications data

        data=soup.find('div',class_='nova-legacy-c-card__body nova-legacy-c-card__body--spacing-none')
        dive=data.find_all('div',class_='nova-legacy-o-stack__item')
    except:
        logging.info("ERROR in loading the page, please check the input url")
    if data:
        for a in dive:
            footer=a.find('div',class_='nova-legacy-v-publication-item__footer')
            datadrill=footer.find_all(lambda tag: tag.name == 'a' and tag.has_attr('href'))
            for link in datadrill:
                href=link['href']
                time.sleep(10)
                subsoup=(rd(href))
                subsoup = BeautifulSoup(subsoup, 'html.parser')
                #Publish type
                pub=subsoup.find('span',class_="nova-legacy-e-badge nova-legacy-e-badge--color-green nova-legacy-e-badge--display-inline nova-legacy-e-badge--luminosity-high nova-legacy-e-badge--size-l nova-legacy-e-badge--theme-solid nova-legacy-e-badge--radius-m research-detail-header-section__badge")
                pubType=pub.get_text()
                #title
                Title=subsoup.find('h1', class_='nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900 research-detail-header-section__title')
                Title=Title.get_text()
                more=subsoup.find('div', class_='research-detail-header-section__ie11')
                listli=[]
                for i in more.find_all('li'):
                    lidata=i.get_text()
                    listli.append(lidata)
                Date=listli[0]
                journal=listli[1]
                journalText, journalCitations=split(journal)
                if re.search(r'\W', journalCitations):  # \W matches any symbols (equivalent to [^a-zA-Z0-9_])
                    journalCitations=journalCitations.strip()
                else:
                    journalCitations=" "
                Abs=subsoup.find('div',class_='nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-800 research-detail-middle-section__abstract')
                if Abs:
                    abstract=Abs.get_text()
                else:
                    abstract=" "
                authlist=subsoup.find_all("div", class_='nova-legacy-l-flex__item research-detail-author-list__item research-detail-author-list__item--small-avatar') 
                if authlist==[]:
                    authlist=subsoup.find_all("div", class_='nova-legacy-l-flex__item research-detail-author-list__item research-detail-author-list__item--has-image')
                for index, item in enumerate(authlist):
                    aname=item.find("div", class_='nova-legacy-v-person-list-item__align-content')
                    authorName=aname.get_text()
                    if index==len(authlist)-1:
                        authorOrder="Last Author"
                    else:
                        authorOrder=str(index+1)+" Author"
                    if index == 11:
                        break
                    if Date.split(" ")[-1].isdigit() and int(Date.split(" ")[-1])>int(noOfYears):
                        shotput=[]
                        shotput.append(ProfileName)
                        shotput.append(OrgName)
                        shotput.append(Title)
                        shotput.append(pubType)
                        shotput.append(authorName)
                        shotput.append(authorOrder)
                        shotput.append(Date)
                        shotput.append(journalText)
                        shotput.append(journalCitations)
                        shotput.append(abstract)
                        shotput.append(href)
                        output.append(shotput)
        return output
    else:
        logging.info("Error: Could not find Publisher Href")
        return output


def search_scrapper(soup,noOfYears,searchkey):
    output=[]
    #publications data
    try:                 
        data=soup.find('div',class_='nova-legacy-o-stack nova-legacy-o-stack--gutter-xs nova-legacy-o-stack--spacing-none nova-legacy-o-stack--no-gutter-outside')
        dive=data.find_all('div',class_='nova-legacy-o-stack__item')

        if data:
            for a in dive:
                footer=a.find('div',class_='nova-legacy-e-text nova-legacy-e-text--size-l nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-inherit nova-legacy-v-publication-item__title')
                datadrill=footer.find_all(lambda tag: tag.name == 'a' and tag.has_attr('href'))
                for link in datadrill:
                    href=link['href']
                    time.sleep(10)
                    subsoup=(rd("https://www.researchgate.net/"+str(href)))
                    subsoup = BeautifulSoup(subsoup, 'html.parser')
                    #Publish type
                    pub=subsoup.find('span',class_="nova-legacy-e-badge nova-legacy-e-badge--color-green nova-legacy-e-badge--display-inline nova-legacy-e-badge--luminosity-high nova-legacy-e-badge--size-l nova-legacy-e-badge--theme-solid nova-legacy-e-badge--radius-m research-detail-header-section__badge")
                    pubType=pub.get_text()
                    #title
                    Title=subsoup.find('h1', class_='nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900 research-detail-header-section__title')
                    Title=Title.get_text()
                    more=subsoup.find('div', class_='research-detail-header-section__ie11')
                    listli=[]
                    for i in more.find_all('li'):
                        lidata=i.get_text()
                        listli.append(lidata)
                    Date=listli[0]
                    journal=listli[1]
                    journalText, journalCitations=split(journal)
                    if re.search(r'\W', journalCitations):  # \W matches any symbols (equivalent to [^a-zA-Z0-9_])
                        journalCitations=journalCitations.strip()
                    else:
                        journalCitations=" "
                    Abs=subsoup.find('div',class_='nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-800 research-detail-middle-section__abstract')
                    if Abs:
                        abstract=Abs.get_text()
                    else:
                        abstract=" "
                    authlist=subsoup.find_all("div", class_='nova-legacy-l-flex__item research-detail-author-list__item research-detail-author-list__item--small-avatar') 
                    if authlist==[]:
                        authlist=subsoup.find_all("div", class_='nova-legacy-l-flex__item research-detail-author-list__item research-detail-author-list__item--has-image')
                    for index, item in enumerate(authlist):
                        aname=item.find("a", class_='nova-legacy-e-link nova-legacy-e-link--color-inherit nova-legacy-e-link--theme-bare')
                        authorName=aname.get_text()
                        if index==len(authlist)-1:
                            authorOrder="Last Author"
                        else:
                            authorOrder=str(index+1)+" Author"
                        if index == 11:
                            break
                        if Date.split(" ")[-1].isdigit() and int(Date.split(" ")[-1])>int(noOfYears):
                            shotput=[]
                            shotput.append(searchkey)
                            shotput.append(Title)
                            shotput.append(pubType)
                            shotput.append(authorName)
                            shotput.append(authorOrder)
                            shotput.append(Date)
                            shotput.append(journalText)
                            shotput.append(journalCitations)
                            shotput.append(abstract)
                            shotput.append(href)
                            output.append(shotput)
            return output
        else:
            logging.info("Error: Could not find Publisher Href")
    except:
        logging.info("ERROR in loading the page or key word search limit exceeded")
        return output

def contributor_scrapper(soup,noOfYears):
    output=[]
    try:
        #Name
        #Name = soup.find('div', class_='nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-xxs nova-legacy-e-text--color-inherit')
        Name = soup.find('h1', class_='nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-600 sci-con__header-title')
        spanNames=[]
        for i in Name.find_all('span'):
            spanData=i.get_text()
            spanNames.append(spanData)
        ProfileName=spanNames[0]
        OrgName=spanNames[1]
        #publications data
        data=soup.find('div',class_='nova-legacy-c-card__body nova-legacy-c-card__body--spacing-none')
        dive=data.find_all('div',class_='nova-legacy-o-stack__item')
    except:
        logging.info("ERROR in loading the page, please check the input url")
    if data:
        for a in dive:
            footer=a.find('div',class_='nova-legacy-v-publication-item__footer')
            datadrill=footer.find_all(lambda tag: tag.name == 'a' and tag.has_attr('href'))
            for link in datadrill:
                href=link['href']
                time.sleep(10)
                if href.startswith("https"):
                    subsoup=(rd(href))
                elif "publication/" in href:
                    parts = href.split('/')
                    result = '/'.join(parts[:2])
                    subsoup=(rd("https://www.researchgate.net/"+str(result)))
                else:
                    continue
                subsoup = BeautifulSoup(subsoup, 'html.parser')
                #Publish type
                pub=subsoup.find('span',class_="nova-legacy-e-badge nova-legacy-e-badge--color-green nova-legacy-e-badge--display-inline nova-legacy-e-badge--luminosity-high nova-legacy-e-badge--size-l nova-legacy-e-badge--theme-solid nova-legacy-e-badge--radius-m research-detail-header-section__badge")
                pubType=pub.get_text()
                #title
                Title=subsoup.find('h1', class_='nova-legacy-e-text nova-legacy-e-text--size-xl nova-legacy-e-text--family-display nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-900 research-detail-header-section__title')
                Title=Title.get_text()
                more=subsoup.find('div', class_='research-detail-header-section__ie11')
                listli=[]
                for i in more.find_all('li'):
                    lidata=i.get_text()
                    listli.append(lidata)
                Date=listli[0]
                journal=listli[1]
                journalText, journalCitations=split(journal)
                if re.search(r'\W', journalCitations):  # \W matches any symbols (equivalent to [^a-zA-Z0-9_])
                    journalCitations=journalCitations.strip()
                else:
                    journalCitations=" "
                Abs=subsoup.find('div',class_='nova-legacy-e-text nova-legacy-e-text--size-m nova-legacy-e-text--family-sans-serif nova-legacy-e-text--spacing-none nova-legacy-e-text--color-grey-800 research-detail-middle-section__abstract')
                if Abs:
                    abstract=Abs.get_text()
                else:
                    abstract=" "
                authlist=subsoup.find_all("div", class_='nova-legacy-l-flex__item research-detail-author-list__item research-detail-author-list__item--small-avatar') 
                if authlist==[]:
                    authlist=subsoup.find_all("div", class_='nova-legacy-l-flex__item research-detail-author-list__item research-detail-author-list__item--has-image')
                for index, item in enumerate(authlist):
                    aname=item.find("div", class_='nova-legacy-v-person-list-item__align-content')
                    authorName=aname.get_text()
                    if index==len(authlist)-1:
                        authorOrder="Last Author"
                    else:
                        authorOrder=str(index+1)+" Author"
                    if index == 11:
                        break
                    if Date.split(" ")[-1].isdigit() and int(Date.split(" ")[-1])>int(noOfYears):
                        shotput=[]
                        shotput.append(ProfileName)
                        shotput.append(OrgName)
                        shotput.append(Title)
                        shotput.append(pubType)
                        shotput.append(authorName)
                        shotput.append(authorOrder)
                        shotput.append(Date)
                        shotput.append(journalText)
                        shotput.append(journalCitations)
                        shotput.append(abstract)
                        shotput.append(href)
                        output.append(shotput)
            print("iteration done")
        return output
    else:
        logging.info("Error: Could not find Publisher Href")
        return output
