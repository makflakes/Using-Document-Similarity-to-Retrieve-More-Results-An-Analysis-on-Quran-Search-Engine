import duplicates
import ranksmodule
import booleanretrieval
import spacymapresults


def max_explanation_sim_suggestion(docids, disjoint_explanations, result_expl_list, new_df, 
                                   max_suggestions=True, print_message=True, return_chap_verse=True):
    
    """
    takes result verses of queries as input and suggests the most similar EXPLANATION as output
    for the top 3 of the input verse list

    Parameters
    ----------
    docids : list
        list of ids for the result verses of queries, can have arbitrary length
    disjoint_explanations: list
        list of all verses (i.e. their explanations) of 
        the results for a query have been "filtered out" by replacing their explanation.
        with an empty string. Every other remainining verse has a vector representation via spaCy's 
        nlp pipeline
    result_expl_list: list
        list of all verses (i.e. their explanations) in the result set for a query. These too have been 
        put through spaCy's nlp pipeline and have a vector representation.
    max_suggestions: bool
        determines whether only the top 3 suggestion or the entire list of suggestions (as long as docids)
        will be returned.
        The default is False.
    print_message: bool
        determines whether a message for the user suggesting top 3 verses should be returned.
        The default is True.
    return_chap_verse: False
        determines whether instead of the list of docids the list of chapter-verse tuples for the 
        suggestions will be returned.
        The default is False.

    Returns
    -------
    extended_docids: list
        list of original docids which is extended by exactly three elements, namely the top 3 suggestions.
        Docids themselves are integers.
    
    """
    
    expl_sims = []
    #print(result_expl_list[0])
    
    for result_expl in result_expl_list: 
        expl_similarities = [result_expl.similarity(expl) for expl in disjoint_explanations]
        expl_similarities[:] = [x if x != 1 else 0 for x in expl_similarities]
        expl_sims.append(expl_similarities)
        
    #print(expl_sims)
    
        
    #get most index of most similar verse for each verse in query result list
    most_sim_expl_index_list = [expl_list.index(max(expl_list)) for expl_list in expl_sims]
    most_sim_chapter_list = [new_df["Chapter"].iloc[expl] for expl in most_sim_expl_index_list]
    most_sim_verse_list = [new_df["Verse"].iloc[expl] for expl in most_sim_expl_index_list]
    most_sim_tuple_list = list(zip(most_sim_chapter_list, most_sim_verse_list))
    
    #remove duplicates --> since order will be preserved, list will skip to next highest ranked elem
    most_sim_expl_index_list_cleaned = duplicates.remove_list_duplicates(most_sim_expl_index_list)
    most_sim_tuple_list_cleaned = duplicates.remove_list_duplicates(most_sim_tuple_list)
    
    #append docids of top 3 suggestions to docids
    extended_docids = docids.copy()
    for index in most_sim_expl_index_list_cleaned[:3]:
        extended_docids.append(index)
    
    #set to True if more than 3 results suggestions shall be returned
    if max_suggestions is False:
        final_chap_verse_tup_list = most_sim_tuple_list_cleaned
        for elem in most_sim_expl_index_list_cleaned:
            extended_docids.append(elem)
    else:
        final_chap_verse_tup_list = most_sim_tuple_list_cleaned[:3]
    
    if print_message is False:
        return extended_docids
    #else:
        #print("You might also be interested in the following verses: \n")
        #print("\n".join("Chapter {}, Verse {}".format(*tup) for tup in final_chap_verse_tup_list))
    
    if return_chap_verse is True:
        return final_chap_verse_tup_list
    else:
        return extended_docids

def max_verse_sim_suggestion(docids, disjoint_verses, result_verse_list, new_df,
                             max_suggestions=True, print_message=True, return_chap_verse=True):
    """
    takes result verses of queries as input and suggests the most similar verse as output
    for the top 3 of the input verse list

    Parameters
    ----------
    docids : list
        list of ids for the result verses of queries, can have arbitrary length
    all_verses: list
        list of all verses where each element is a string, namely the verse itself
    max_suggestions: bool
        determines whether only the top 3 suggestion or the entire list of suggestions (as long as docids)
        will be returned.
        The default is False.
    print_message: bool
        determines whether a message for the user suggesting top 3 verses should be returned.
        The default is True.

    Returns
    -------
    extended_docids: list
        list of original docids which is extended by exactly three elements, namely the top 3 suggestions.
        Docids themselves are integers.
    
    """
        
    verse_sims = [] #create list of verse similarities for each verse
    for result_verse in result_verse_list:
        similarities = [result_verse.similarity(verse) for verse in disjoint_verses]
        similarities[:] = [v if v != 1 else 0 for v in similarities]
        verse_sims.append(similarities)
        
    #get max elements of each verse list only (for suggestions) --> most similar verse for each verse
    most_sim_index_list = [verse_list.index(max(verse_list)) for verse_list in verse_sims]
    #get chapter numbers of each most simlar verse
    most_sim_chapter_list = [new_df["Chapter"].iloc[most_sim] for most_sim in most_sim_index_list]
    #get verse numbers of each most similar verse
    most_sim_verse_list = [new_df["Verse"].iloc[most_sim] for most_sim in most_sim_index_list]
    most_sim_tuple_list = list(zip(most_sim_chapter_list, most_sim_verse_list))
    
    #remove duplicates --> since order will be preserved, list will skip to next highest ranked elem
    most_sim_index_list_cleaned = duplicates.remove_list_duplicates(most_sim_index_list)
    most_sim_tuple_list_cleaned = duplicates.remove_list_duplicates(most_sim_tuple_list)
       
    #append docids of top 3 suggestions to docids
    extended_docids = docids.copy()
    for index in most_sim_index_list_cleaned[:3]:
        extended_docids.append(index)
    
    #set to True if more than 3 results suggestions shall be returned
    if max_suggestions is False:
        final_chap_verse_tup_list = most_sim_tuple_list_cleaned
        for elem in most_sim_index_list_cleaned:
            extended_docids.append(elem)
    else:
        final_chap_verse_tup_list = most_sim_tuple_list_cleaned[:3]
    
    #decide whether message will be printed or not
    if print_message is False:
        return extended_docids
    #else:
        #print("You might also be interested in the following verses: \n")
        #print("\n".join("Chapter {}, Verse {}".format(*tup) for tup in final_chap_verse_tup_list))
    
    if return_chap_verse is True:
        return final_chap_verse_tup_list
    else:
        return extended_docids

def inverted_verse_results(query, disjoint_verses, invindex, new_df, tokenwords, postlist, tfidfVector, nlp, all_words):
    
    query_dict = {}
    i=0
        
    query_list, chapvers, docids = booleanretrieval.boolean_retrieval(query, invindex, new_df, tokenwords, postlist, tfidfVector, all_words)
    #print(docids)
    ranks, chapvers = ranksmodule.ranking(docids, query_list, new_df, tfidfVector)
        
    result_verse_list, all_verses = spacymapresults.verse_spacy_map(ranks, nlp, new_df)
    #print(result_verse_list)
        
    max_verse_suggestion = max_verse_sim_suggestion(ranks, disjoint_verses, result_verse_list, new_df)
        
    list=[]
    for suggestions in max_verse_suggestion:
        #print(suggestions)
        list.append(suggestions)
        
    #print(ranks)
    query_dict[query] = ranks
        
    print('\n')
        
    return chapvers, max_verse_suggestion

def inverted_explanation_results(query, disjoint_explanations, invindex, new_df, tokenwords, postlist, tfidfVector, nlp, all_words, use_plain_explanations=False):
    """
    
    """
    
    query_dict = {}
    i=0
        
    query_list, chapvers, docids = booleanretrieval.boolean_retrieval(query, invindex, new_df, tokenwords, postlist, tfidfVector, all_words)
    #print(docids)
    ranks, chapvers = ranksmodule.ranking(docids, query_list, new_df, tfidfVector)
        
    result_expl_list, all_explanations = spacymapresults.expl_spacy_map(ranks, nlp, new_df, use_plain_explanations=use_plain_explanations)
        
    max_explanation_suggestion = max_explanation_sim_suggestion(ranks, disjoint_explanations, result_expl_list, new_df)
        
        
    for suggestions in max_explanation_suggestion:
        ranks.append(suggestions)
        
    query_dict[query] = ranks
        
    print('\n')
        
    return chapvers, max_explanation_suggestion

def setting(suggestion, query, disjoint_docs, invindex, new_df, tokenwords, postlist, tfidfVector, nlp, all_words):

    results = []
    suggestedverses = []

    if suggestion=='1':
        results, suggestedverses = inverted_explanation_results(query, disjoint_docs, invindex, new_df, tokenwords, postlist, tfidfVector, nlp, all_words)
    elif suggestion=='2':
        results, suggestedverses = inverted_explanation_results(query, disjoint_docs, invindex, new_df, tokenwords, postlist, tfidfVector, nlp, all_words, use_plain_explanations=True)
    elif suggestion=='3':
        results, suggestedverses = inverted_verse_results(query, disjoint_docs, invindex, new_df, tokenwords, postlist, tfidfVector, nlp, all_words)


    return results, suggestedverses