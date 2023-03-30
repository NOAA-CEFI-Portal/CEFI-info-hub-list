"""
The script is to check the json resource file can be read in correctly

Conda env:
- cefilist 

"""
from generate_readme import get_cefi_list

data = get_cefi_list()
print('json file successfully loaded')