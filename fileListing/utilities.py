import os

def cleanListings():
    base_string = os.path.join(os.getcwd())
    walk_results = os.walk(os.path.join(base_string))
    listing_list = walk_results.next()[-1]
    for file in listing_list:
        if file[-4:]=='.fls':
            os.remove(os.path.join(base_string,file))
    print(" Cleaned")
    
    