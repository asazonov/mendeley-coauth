
# coding: utf-8

# In[4]:

from Bio import Entrez
import os
import json
import sys
import urllib.request

Entrez.email = 'ale@gmail.com'
    
def fetch_xml(pmid):
    handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
    xml_data = Entrez.read(handle)[0]
    try:
        return xml_data
    except IndexError:
        return None

def doi_to_pmid(doi):
    handle = Entrez.esearch(db="pubmed", retmax=100, term=doi)
    record = Entrez.read(handle)
    handle.close()
    try:
        return record['IdList'][0]
    except IndexError:
        return None

def process_mendeley_record(record):
    try: 
        doi = record['doi']
        pmid = doi_to_pmid(doi)
        if pmid != None:
            pubmed_xml = fetch_xml(pmid)

            # Process authors 
            authors = []
            if 'AuthorList' in pubmed_xml['MedlineCitation']['Article'] and 'MedlineCitation' in pubmed_xml:
                for author in pubmed_xml['MedlineCitation']['Article']['AuthorList']:
                    if 'ForeName' in author:
                        fullname = author['ForeName'] + " " + author['LastName']
                    elif 'LastName' in author:
                        fullname = author['LastName']
                    else:
                        return None
                         
                    authors += [fullname]
            else: 
                return None
            
             # Process keywords
            keywords = []

            # Process keywords from Mendeley
            keywords += [x.lower() for x in record['keywords']]

            # Process keyboards from mesh
            if 'MeshHeadingList' in list(pubmed_xml['MedlineCitation']):
                mesh_headings = list(pubmed_xml['MedlineCitation']['MeshHeadingList'])
                for mesh_heading in mesh_headings:
                    if mesh_heading['DescriptorName'].attributes['MajorTopicYN'] == 'Y':
                        keywords += [str(mesh_heading['DescriptorName']).lower()]
                    qualifier = mesh_heading['QualifierName']
                    if len(qualifier) > 0 and qualifier[0].attributes['MajorTopicYN'] == 'Y':
                        keywords += [str(qualifier[0]).lower()]

            # Process keywords from Pubmed
            if 'KeywordList' in pubmed_xml['MedlineCitation'] and len(pubmed_xml['MedlineCitation']['KeywordList']) > 0:
                for keyword in pubmed_xml['MedlineCitation']['KeywordList'][0]:
                    keywords += [keyword.lower()]
            
            keywords = list(set(keywords))
            
            return {'authors':authors, 'keywords':keywords}
        else:
            return None
    except urllib.error.HTTPError as err:
        print(err.code)
        return None

# In[6]:

def main():
    #for i in os.listdir('./data'):
    #    if i.endswith(".json"): 
    json_file = open('./data/' + sys.argv[1])
    mendeley_data = json.load(json_file)
    output_file = open('./data_out/' + sys.argv[1], 'w')
    for i, record in enumerate(mendeley_data):
        record_output = process_mendeley_record(record)
        if record_output is not None:
            output_file.write(str(record_output) + '\n')
            if i % 30 == 0:
                output_file.flush()
                print(i)
    output_file.close()
#             continue
#         else:
#             continue
    
    
if __name__ == "__main__":
    main()

