import streamlit as st
import requests
import re


# FUNCTION DEFINITIONS

def split_input(txt):
    '''Splits the input into a list of domains. No error checking.'''
    return re.split(r'[,;\n]', txt)

def create_img_list(domains):
    '''Converts list of domains into Image URLs that pull from the clearbit API. If a domain is not provided,
    then try and resolve with Clearbit Autocomplete API.'''
     
    prefix_logo = 'https://logo.clearbit.com/'
    prefix_info = 'https://autocomplete.clearbit.com/v1/companies/suggest?query='
    
    urls = []
    for d in domains:
        if valid_domain(d):
            urls.append((prefix_logo + d, d))
        else:
            # get possible domains
            possible_domains = requests.get(prefix_info + d).json()
            
            # for each domain, append to urls list
            for p in possible_domains:
                urls.append((p['logo'], d + ' (guess: ' + p['domain'] + ')'))
            
    return urls

def valid_domain(domain):
    '''Check string to determine if it's a valid domain'''
    
    pattern = "^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|([a-zA-Z0-9][a-zA-Z0-9-_]{1,61}[a-zA-Z0-9]))\.([a-zA-Z]{2,6}|[a-zA-Z0-9-]{2,30}\.[a-zA-Z]{2,3})$"
    return bool(re.match(pattern, domain))


# STREAMLIT CODE
st.header("Logo Grabber")
st.write("Get logos in bulk for sales decks! (Version 1.2)")
txt = st.text_area('Enter a list of domains or search terms, separated by commas, semicolons, or new lines:', 
                   'snowflake.com,robling.io,procter gamble\nkraftheinz.com;albertsons.com', 
                   placeholder='''Type a list of 
                   Company URLs separated by 
                   commas (e.g. snowflake.com,
                   robling.io). Do not put www 
                   in front.''')

# Get list of inputs and translate to Logo URLs or autocompletes
companies = split_input(txt)
request_list = create_img_list(companies)

# Parse (url, caption) tuples
urls = []
captions = []
for r in request_list:
    urls.append(r[0])
    captions.append(r[1])

# Plot matrix of logots
st.image(image=urls, caption=captions)

# Credits and Notes
st.markdown('*Known issues: No error-checking on text entry, no graceful fail for 404, no grayscaled images, no default sizes for images.*')
st.markdown('[Logos provided by Clearbit](https://clearbit.com)')
st.markdown('Created by [Prabhath Nanisetty](https://www.linkedin.com/in/prabhathnanisetty). Code at [Github](https://github.com/prabhathn/logo_grabber)')
