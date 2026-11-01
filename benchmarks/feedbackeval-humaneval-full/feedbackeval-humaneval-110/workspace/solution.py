def exchange(lst1, lst2):
    evens_in_lst1 = sum(1 for num in lst1 if num % 2 == 0)
    evens_in_lst2 = sum(1 for num in lst2 if num % 2 == 0)
    
    return "YES" if evens_in_lst1 <= evens_in_lst2 else "NO"
