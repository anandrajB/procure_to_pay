from transaction.states import StateChoices
from transaction.models import workevents, workflowitems
from viewflow import fsm
from accounts.models import CounterParty, Parties
from transaction.FSM.query_handler import (
    gets_wf_item_id
)

class CounterPartyFlow(object):
    # workitems = workflowitems()
    stage = fsm.State(StateChoices, default=StateChoices.STATUS_DRAFT)
    bank = Parties.objects.get(party_type="BANK")
    

    def __init__(self, workflowitems):
        self.workflowitems = workflowitems

    @stage.setter()
    def _set_status_stage(self, value):
        self.workflowitems.initial_state = value

    @stage.getter()
    def _get_status(self):
        return self.workflowitems.initial_state




    def gets_parties(self):
        query = Parties.objects.get(name = self.workflowitems.counterparty.name , city = self.workflowitems.counterparty.city)
        return query

# ------------------------#
#  DRAFT       TRANSITION #
# ------------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def Draft_flow(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        
        self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.interim_state = StateChoices.STATUS_DRAFT
        Parties.objects.filter(name = self.workflowitems.counterparty.name , city = self.workflowitems.counterparty.city).update(status = StateChoices.IN_PROGRESS)
        self.workflowitems.counterparty.onboarding = StateChoices.STATUS_DRAFT
        self.workflowitems.current_from_party = self.workflowitems.current_to_party = user.party
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, type="COUNTERPARTY_ONBOARING", event_user = user ,comments = self.workflowitems.comments,
                                  interim_state=StateChoices.STATUS_DRAFT, from_party=self.workflowitems.current_from_party, to_party=self.workflowitems.current_to_party)
    
        cs.save()
        # if user.party.party_type == "BANK":
        #     cs.to_party = self.workflowitems.user.party
        #     self.workflowitems.current_to_party = self.workflowitems.user.party
        #     cs.save()
        # else:
        #     self.workflowitems.current_to_party = self.bank
        #     cs.to_party = self.bank
        #     cs.save()




# --------------------------#
#  SENT_TO_BANK  TRANSITION #
# --------------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.STATUS_DRAFT)
    def sent_to_bank(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.interim_state = StateChoices.SENT_TO_BANK
        self.workflowitems.current_from_party = user.party
        self.workflowitems.current_to_party = self.bank
        Parties.objects.filter(name = self.workflowitems.counterparty.name , city = self.workflowitems.counterparty.city).update(status = StateChoices.DEACTIVATED)
        CounterParty.objects.filter(name = self.workflowitems.counterparty.name , city = self.workflowitems.counterparty.city).update(onboarding = StateChoices.SENT_TO_BANK)
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.STATUS_DRAFT, to_state=StateChoices.STATUS_COMPLETED, type="COUNTERPARTY_ONBOARING", event_user = user ,
        comments = self.workflowitems.comments,final = "YES" , interim_state=StateChoices.SENT_TO_BANK, from_party=self.workflowitems.current_from_party, to_party= self.bank)
        # to_party goes to bank
        cs.save()



# ----------------------------------#
#  SENT_TO_COUNTERPARTY  TRANSITION #
# ----------------------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.SENT_TO_BANK)
    def sent_to_counterparty(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.interim_state = StateChoices.SENT_TO_COUNTERPARTY
        self.workflowitems.current_from_party = self.bank
        self.workflowitems.current_to_party = user.party
        self.workflowitems.final = "YES"
        Parties.objects.filter(name = self.workflowitems.counterparty.name , city = self.workflowitems.counterparty.city).update(status = StateChoices.IN_PROGRESS)
        CounterParty.objects.filter(name = self.workflowitems.counterparty.name , city = self.workflowitems.counterparty.city).update(onboarding = StateChoices.SENT_TO_COUNTERPARTY)
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.SENT_TO_BANK, to_state=StateChoices.STATUS_COMPLETED, type="COUNTERPARTY_ONBOARING", event_user = user ,comments = self.workflowitems.comments,
                                  interim_state=StateChoices.SENT_TO_COUNTERPARTY, final = "YES" , from_party = self.bank , to_party= user.party)
        # to_party goes to bank
        cs.save()




# ----------------------#
#  REJECT    TRANSITION #
# ----------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.SENT_TO_BANK)
    def reject(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        self.workflowitems.final_state = StateChoices.STATUS_REJECTED
        self.workflowitems.interim_state = StateChoices.STATUS_REJECTED
        self.workflowitems.current_from_party , self.workflowitems.current_to_party = self.bank , user.party
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.SENT_TO_BANK, to_state=StateChoices.STATUS_REJECTED, type="COUNTERPARTY_ONBOARING", event_user = user ,comments = self.workflowitems.comments,
                                  interim_state=StateChoices.STATUS_REJECTED, from_party = self.bank , to_party= user.party)
        # to_party goes to bank
        cs.save()


# ----------------------#
#  COMPLETE  TRANSITION #
# ----------------------#

    @stage.transition(source=stage.ANY, target=StateChoices.SENT_TO_BANK)
    def complete(self,request):
        user = request.user
        ws = gets_wf_item_id(self.workflowitems.id)
        self.workflowitems.final_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.interim_state = StateChoices.STATUS_COMPLETED
        self.workflowitems.current_from_party = self.bank
        self.workflowitems.current_to_party = user.party
        Parties.objects.filter(name = self.workflowitems.counterparty.name , city = self.workflowitems.counterparty.city).update(status = StateChoices.ONBOARDED)
        CounterParty.objects.filter(name = self.workflowitems.counterparty.name , city = self.workflowitems.counterparty.city).update(onboarding = StateChoices.STATUS_COMPLETED)
        cs = workevents.objects.create(workitems=ws, from_state=StateChoices.SENT_TO_BANK, to_state=StateChoices.STATUS_COMPLETED, type="COUNTERPARTY_ONBOARING", event_user = user ,comments = self.workflowitems.comments,
                                  interim_state=StateChoices.STATUS_COMPLETED ,from_party = self.bank , to_party= user.party)
        # to_party goes to bank
        cs.save()
