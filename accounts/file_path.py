

### FILE ROOT DIRECTORY HANDLER FUNCTION



def profile_img_path(instance, filename):
    return "finflo/media/user/{email}/{filename}".format( email = instance.email ,filename=filename)

# def party_img_path(instance, filename):
#     return "accounts/party_pic/{}/{email}/{filename}".format( email = instance.email ,filename=filename)



# TRANSACTION - APP


def program_file_path(instance,filename):
    return 'scf/program/{0}/{1}'.format(instance.party.name , filename)


def pairing_file_path(instance,filename):
    return 'scf/pairing/user_{0}/{1}/{2}'.format(instance.counterparty_id.id , instance.counterparty_id.name , filename)


def invoice_upload_file_path(instance,filename):
    return 'scf/invoice_attachements/{0}'.format(filename)


def manage_scf_attachments(instance,filename):
    return 'finflo/media/attachments/{0}'.format(filename)
