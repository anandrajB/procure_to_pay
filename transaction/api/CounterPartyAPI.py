from rest_framework import status
from transaction.models import workflowitems, workevents , Pairings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import generics
from transaction.FSM.Invoice import InvoiceFlow
from accounts.models import CounterParty, Parties
from rest_framework import serializers

# -----------------------------------
#       COUNTERPARTY TRANSITIONS
# -----------------------------------


class CounterPartyTransitionAPIView(APIView):
    queryset = workflowitems.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        obj = generics.get_object_or_404(CounterParty, id=pk)
        initial_state = request.data.get('initial_state')
        interim_state = request.data.get('interim_state')
        final_state = request.data.get('final_state')
        from_party = request.data.get('from_party')
        to_party = request.data.get('to_party')
    
        if obj:

            counterparty = CounterParty.objects.get(id=obj.id)
            Party = Parties.objects.get(name = counterparty.name , city = counterparty.city)
            banks = Parties.objects.get(party_type="BANK")
            obj , created  = workflowitems.objects.update_or_create(
                counterparty=counterparty, defaults={'user': user, 'current_from_party': Party if from_party else banks, 'current_to_party': Party if to_party else banks, 'initial_state': initial_state, 'interim_state': interim_state, 'final_state': final_state})
            workevents.objects.create(
                workitems=obj, event_user=user, from_party = Party if from_party else banks, to_party= Party if to_party else banks, from_state=initial_state, to_state=final_state, interim_state=interim_state)
    
            return Response({"status": "success", "data": "success "}, status=status.HTTP_200_OK)

        return Response({"status": "failure", "data": "can't do this transition "}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)







class counterpartymessageserializer(serializers.ModelSerializer):
    current_from_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    current_to_party = serializers.SlugRelatedField(read_only=True, slug_field='name')
    wf_item_id = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(read_only=True, slug_field='email')
    record_datas = serializers.SerializerMethodField()

    class Meta:
        model = workflowitems
        fields = [
            'wf_item_id',
            'counterparty',
            'initial_state',
            'interim_state',
            'final_state',
            'next_available_transitions',
            'current_from_party',
            'current_to_party',
            'user',
            'created_date',
            'action',
            'record_datas',
            'type',
            'subaction',
            'previous_action',

        ]

    def get_wf_item_id(self,obj):
        return obj.id

    def get_record_datas(self,obj):
        try:
            pair = Pairings.objects.filter(counterparty_id = obj.counterparty.id).values()
            if obj.type == "COUNTERPARTY":
                qs = CounterParty.objects.filter(workflowitems = obj.id).values()
            return {"model": qs, "pairing": pair }
        except:
            return None
    




class CounterPartyMessageListApiViw(ListAPIView):
    permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
        var = workflowitems.objects.filter(counterparty__name = "RENAULT")
        serializer = counterpartymessageserializer(var, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
