import os, sys
path = os.path.join(os.path.dirname(__file__), '../..')
sys.path.insert(0,path)
import api.spot_api as asp
sys.path.pop(0)

test= asp.SpotApi()
dico={}
response = test.list_currency_pairs( )
# Print the response
print(f"list_currency_pairs: {response}\n\n\n\n")
