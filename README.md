# Information-Retrieval-on-Quran-Verses
Computational Linguistics Team Lab Project, SS 2022 </br>
Authors : Mohammed Abdul Khaliq, Ufkun-Bayram Menderes, Muhammad Saad Magdi </br>

## Prerequisites
Please make sure to download the relevant libraries from requirements.txt file :
```
pip3 install requirements.txt
```
For this code to work properly, it is essential to have spaCy version 2.3.x.</br>
If it isnt already downloaded, run the following command :
```
pip3 install -U spacy==2.3.7
```
Then download the spaCy en_core_web_lg module with the following lines of code:
```
import spacy.cli
spacy.cli.download("en_core_web_lg")
```

## Running the code
This code is available in both python3 `/src` and jupyter-notebook `/jupyter`.
The code can be run using the pretrained and computed data structures or running it from scratch.

### Precomputed vectors and data structures
To run the code from pretrained data, you will have to download the pickle files from : [Pretrained Data](https://drive.google.com/drive/folders/1DWARVZnnqjK4xeCS3KTQ4b5Ky_EU_Ikz?usp=sharing) and place them in the `\pickle` folder of the repository.

### Running in jupyter-notebook
Download the repository and open jupyter-notebook file present in `/jupyter/Quran Search Engine.ipynb`.</br>
The first cell of this notebook has some important variables that can be tinkered with to make use of either pretrained data or to run the program from scratch. In addition, a variable is also defined to use each of the 3 verse suggestion setting the user decides to choose from. </br>
- **use_loaded_inverted_index** : set this value to 1 to use pretrained invertedindex, 0 to create the inverted index from scratch.
- **use_loaded_tfidf** : set this value to 1 to use pretrained tfidf vectors, 0 to create tfidf vectors from scratch
- **use_loaded_spacy_maps** : set this value to 1 to use pretrained spaCy objects, 0 to create spaCy objects in real time.
- **use_verse_suggestion** : 1 for 'verse similarity', 2 for 'preprocessed explanation similarity', 3 for 'unpreprocessed explanation simialrity'







