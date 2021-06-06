# Gets the model, unpack and save it
import requests
import tarfile
import os, sys

# do the request
print('Getting model')
url = 'https://vallant.in/models/en_medical_ner_reddit.tar.gz'
r = requests.get(url, allow_redirects=True)

# save the content
print('Saving model')
open('nerflask/en_medical_ner_reddit.tar.gz', 'wb').write(r.content)

# untar
print('Unpacking model')
my_tar = tarfile.open('nerflask/en_medical_ner_reddit.tar.gz')
my_tar.extractall('nerflask') # specify which folder to extract to
my_tar.close()

#rename dir
os.rename("nerflask/model-best","nerflask/model")

# remove tar file
os.remove("nerflask/en_medical_ner_reddit.tar.gz")
print('Done with the model')