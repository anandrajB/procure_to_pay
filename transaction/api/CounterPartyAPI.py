from accounts.permission.base_permission import Is_Bank, Is_Buyer, Is_Seller
from accounts.models import signatures, userprocessauth
from transaction.FSM.invoice_bank import InvoiceBankFlow
from rest_framework import status
from transaction.models import workflowitems, workevents
from rest_framework.permissions import IsAuthenticated
from transaction.serializer import Workitemserializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from transaction.FSM.Invoice import InvoiceFlow
from accounts.models import CounterParty


# -----------------------------------
#       COUNTERPARTY TRANSITIONS
# -----------------------------------


class CounterPartyTransitionAPIView(APIView):
    queryset = workflowitems.objects.all()
    permission_classes = [Is_Buyer | Is_Bank]

    def post(self, request, pk, *args, **kwargs):
        user = request.user

        counterparty_id = request.data.get('counterparty_id')
        initial_state = request.data.get('initial_state')
        interim_state = request.data.get('interim_state')
        final_state = request.data.get('final_state')

        if counterparty_id:

            counterparty = CounterParty.objects.get(id=counterparty_id)

            wf = workflowitems.objects.update_or_create(
                counterparty=counterparty, defaults={'user': user, 'current_from_party': user.party, 'current_to_party': user.party, 'initial_state': initial_state, 'interim_state': interim_state, 'final_state': final_state})

            workevents.objects.create(
                workitems=wf, event_user=user, from_party=user.party, to_party=user.party, from_state=initial_state, to_state=final_state, interim_state=interim_state)

            return Response({"status": "success", "data": "initial submit success "}, status=status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
