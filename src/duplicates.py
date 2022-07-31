

def remove_list_duplicates(lst):
    """
    takes any list with any sort of elements and maintains only unique element of the input list
    while maintaining original list order
    
    Parameters
    ----------
    lst: list
        any list with any number of elements and any sort of elements
    
    Returns
    -------
    cleaned_list: list
        The original list with the same order where duplicate elements have been removed
    """
    seen_set = set()
    cleaned_list = [elem for elem in lst if elem not in seen_set and not seen_set.add(elem)]
    return cleaned_list