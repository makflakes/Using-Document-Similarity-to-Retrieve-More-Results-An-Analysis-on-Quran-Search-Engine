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
The code can be run using the pretrained and computed data structures or running it from scratch.

### Running from precomputed vectors and data structures
To run the code from pretrained data, you will have to download the pickle files from : https://drive.google.com/drive/folders/1DWARVZnnqjK4xeCS3KTQ4b5Ky_EU_Ikz?usp=sharing and place them in the `\pickle` folder of the repository.

