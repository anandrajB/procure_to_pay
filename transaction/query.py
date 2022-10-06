from accounts.models import Currencies , Parties
from .models import Pairings , Programs


def gets_currencies(values):
    return Currencies.objects.get(description = values)
    
def gets_party(id):
    query = Parties.objects.get(name  = id)
    return query

def gets_party_id(id):
    query = Parties.objects.get(id  = id)
    return query
     
def gets_pairings(id):
    cs = Pairings.objects.get(id=id)
    return cs