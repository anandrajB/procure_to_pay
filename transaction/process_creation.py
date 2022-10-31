# from accounts.models import Action, signatures , userprocessauth

# def gets_action(*args):
#     return Action.objects.get(desc = args)

# def creates_base_sign_for_users(party , user ):

#     sign = signatures.objects.bulk_create([
#     signatures(model="INVOICE",action = gets_action("REQUEST FINANCE"), party = party,sign_a = True , sign_b = False , sign_c = False),
#     signatures(model="INVOICE" , action = gets_action("SUBMIT"),party = party ,sign_a = True , sign_b = False , sign_c = False),
#     signatures(model="UPLOAD" , action = gets_action("SUBMIT"),party = party, sign_a = True , sign_b = False , sign_c = False)
#     ])
#     sign.save()
#     process = userprocessauth.objects.bulk_update([
#         userprocessauth(user = user , model = "INVOICE" , action=gets_action("REQUEST FINANCE") , data_entry = True , sign_a = True , sign_b = True , sign_c = True),
#         userprocessauth(user = user , model = "INVOICE" , action= gets_action("SUBMIT"), data_entry = True , sign_a = True , sign_b = True , sign_c = True),
#         userprocessauth(user = user , model = "UPLOAD" , action=gets_action("SUBMIT") , data_entry = True , sign_a = True , sign_b = True , sign_c = True)
#     ])
#     process.save()