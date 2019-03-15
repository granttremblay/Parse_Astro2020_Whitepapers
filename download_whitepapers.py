#!/usr/bin/env python

# A quick script by Grant Tremblay
# You might need to download (and rename, or otherwise change the filename below)
# the CSV file here:
# http://sites.nationalacademies.org/SSB/CurrentProjects/SSB_185159#community_input

import requests
from astropy.io import ascii

table = ascii.read('all_astro2020_whitepapers.csv')

numbers = table['Response ID']
people = table['Last Name:Principal Author']
urls = table['1:Upload File']

for number, person, url in zip(numbers, people, urls):
    # Most papers are PDFs, but a few are MS Word .docx files
    if url[-4:] == ".pdf":
        try:
            pdf = requests.get(url, allow_redirects=True)
            open('{}_{}.pdf'.format(number, person), 'wb').write(pdf.content)
            print('Downloaded {}_{}.pdf'.format(
                number, person.replace(' ', '-')))
        except:
            print('ERROR downloading {}'.format(url))

    elif url[-5:] == ".docx":
        try:
            docx = requests.get(url, allow_redirects=True)
            open('{}_{}.docx'.format(number, person), 'wb').write(docx.content)
            print('Downloaded {}_{}.docx'.format(
                number, person.replace(' ', '-')))
        except:
            print('ERROR downloading {}'.format(url))
    else:
        print('Something is wrong with the URL for {}. Skipping it.'.format(person))

print("Downloads complete. REMEMBER TO CONVERT THE .docx WORD FILES TO PDF!")
print("If you're on macOS, do this with './convert_docx_to_pdf.sh *.docx")
print("Otherwise, you can of course do it manually.")
