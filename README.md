# Using Document Similarity to Retrieve More Results : An Analysis on Quran Search Engine
Computational Linguistics Team Lab Project, SS 2022 </br>

**Authors** : </br> 
- Mohammed Abdul Khaliq (st181091@stud.uni-stuttgart.de) 
- Ufkun-Bayram Menderes (st181325@stud.uni-stuttgart.de)
- Muhammad Saad Magdi (st176978@stud.uni-stuttgart.de) 

## Dataset
The dataset used for our project is the English Translation of the Quran alongwith the Tafsir of Ibn Kathir (https://www.alim.org/quran/tafsir/ibn-kathir/). The dataset available in the repository was constructed by us and has 1137 verses of the Quran alongwith their translation and explanation.

## Program Flow
![Screenshot](/figures/Untitled-1.png)

## Prerequisites
Please make sure to download the relevant libraries from requirements.txt file :
```
pip3 install -r requirements.txt
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
To run the code from pretrained data, you will have to download the pickle files from : [Pretrained Data](https://drive.google.com/drive/folders/1DWARVZnnqjK4xeCS3KTQ4b5Ky_EU_Ikz?usp=sharing) and place them in the `\pickle` folder of the repository. Note that some of the files are already present while the others need to be downloaded.

- ### Running in jupyter-notebook
Download the repository and open jupyter-notebook file present in `/jupyter/Quran Search Engine.ipynb`.</br>
The first cell of this notebook has some important variables that can be tinkered with to make use of either pretrained data or to run the program from scratch. In addition, a variable is also defined to use each of the 3 verse suggestion setting the user decides to choose from. </br>
- **use_loaded_inverted_index** : set this value to 1 to use pretrained invertedindex, 0 to create the inverted index from scratch.
- **use_loaded_tfidf** : set this value to 1 to use pretrained tfidf vectors, 0 to create tfidf vectors from scratch
- **use_loaded_spacy_maps** : set this value to 1 to use pretrained spaCy objects, 0 to create spaCy objects in real time.
- **use_verse_suggestion** : 1 for 'preprocessed explanations', 2 for 'unpreprocessed explanations' and 3 for 'verse similarity'

- ### Running in Python 3
Download the repository and navigate to `\src` folder. </br>
The `main.py` file is the main program that runs the search engine. We have 3 additional command line arguments that determine the setting in which the program is run.

```
python3 main.py 'dataset_path' use_saves verse_suggestion_setting
```

The variables take the following values :</br>
- **'dataset path'** : a string indicating the location of the main dataset (Quran.csv).
- **use_saves** : 1 for using pretrained data, 0 to run from scratch.
- **verse_suggestion_setting** : 1 for 'preprocessed explanations', 2 for 'unpreprocessed explanations' and 3 for 'verse similarity'

A command line argument which makes use of `pretrained data` and uses `verse similarity` for suggestions would look like :
```
python3 main.py '../data/Quran.csv' 1 3
```

A command line argument that runs the program from `scratch` and uses `unpreprocessed explanations` for suggestions would look like :
```
python3 main.py '../data/Quran.csv' 0 2
```
Your code should be good to go and you can now query the search engine.

## Results of Verse Suggestion compared to base Boolean Retrieval Model
Our experiments show a higher recall over the baseline Boolean Retrieval algorithm when making use of document similarity using either of the 3 proposed methods.

| Method                                          | Precision  | Recall    |   F1   |
| ------------------------------------------------| ---------- | ----------|--------|
| Boolean Retrieval                               | 0.44       | 0.43      |0.34    |
| Boolean Retrieval + Preprocessed Expalanations  | 0.36       | **0.51**      |0.30    |
| Boolean Retrieval + Unpreprocessed Expalanations| 0.35       | **0.50**      |0.29    |
| Boolean Retrieval + Verse Translation           | 0.34       | **0.50**      |0.28    |

## Acknowledgements
This paper and implementation were developed for the course "Computational Lingustics Team Labs, 2022" as part of Masters programme in Computational Linguistics at University of Stuttgart. We would like to thank Dr. Roman Klinger and Mr. Yarik Menchaca Resendiz for their continued support, guidance and motivation throughout the course of the proejct.




