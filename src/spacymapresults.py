import pandas as pd



#Mapping the explanations results documents to spaCy 
def expl_spacy_map(docids, nlp, new_df, use_plain_explanations=False):
    
    if use_plain_explanations is True:
        #print('Using plain explanations...')
        all_explanations = new_df["Tafsir"].tolist()
    else: 
        all_explanations = new_df["Clean_Text"].tolist()
        all_explanations = [' '.join(ele) for ele in all_explanations]
        
    
    
    result_expl_list=[]
    
    for i in docids:
        #print(i)
        result_expl_list.append(nlp(all_explanations[i]))

        
    return result_expl_list, all_explanations


#Mapping the verse results documents to spaCy 
def verse_spacy_map(ranks, nlp, new_df):
    
    all_verses = new_df["Translation"].tolist()
    
    result_verse_list = []
    
    for i in ranks:
        #print(i)
        result_verse_list.append(nlp(all_verses[i]))
    
    return result_verse_list, all_verses