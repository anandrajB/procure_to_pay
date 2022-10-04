from django.contrib.auth import get_user_model
from transaction.models import (
    Pairings,
    Programs
)
from .models import (
    Action,
    Banks, 
    Countries,
    Currencies,
    Parties, 
    CounterParty, 
    PhoneOTP, 
    signatures,
    signupprocess, 
    userprocessauth,
    Models , 
)  
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.conf import settings
from rest_framework.validators import UniqueTogetherValidator
from transaction.custom_validators import profile_img_validator

# MY USER MODEL
User = get_user_model()



# OTP SERIALIZER 

class Otpserializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = ['otp']

        
# BANK SERIALIZER

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banks
        fields = '__all__'
    
    def validate_name(self, attrs):
        if Banks.objects.filter(name= attrs).exists():
            raise serializers.ValidationError("bank name already exists")
        return attrs


# PARTY LIST SERIALIZER

class partieserializer(serializers.ModelSerializer):
    country_code = serializers.SlugRelatedField(read_only=True, slug_field='country')
    base_currency = serializers.SlugRelatedField(read_only=True, slug_field='description')


    class Meta:
        model = Parties
        fields = [
            'id',
            'name',
            'customer_id',
            'address_line_1',
            'address_line_2',
            'onboarded',
            'party_type',
            'status',
            'city',
            'base_currency',
            'state',
            'zipcode',
            'country_code',
            'party_type',
        ]

    


# PARTY SIGNUP SERIALIZERS

class PartiesSignupSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Parties
        fields = '__all__'
        extra_kwargs = {
        "customer_id" : {"required": False , "default" : None},
		"address_line_1": {"required": False},
        "address_line_2": {"required": False},
        "city": {"required": False},
        "state": {"required": False},
        "zipcode": {"required": False},
        "status" : {"required": False},
	    }
        validators = [
            UniqueTogetherValidator(
                queryset=Parties.objects.all(),
                fields=['name', 'city'],
                message = "Party with this city already exists"
            )
        ]
    
    # def to_representation(self, instance):
    #     data = super(PartiesSignupSerailizer, self).to_representation(instance=instance)
    #     data['city'] = data['city'].lower() if data['city'] else data['city']
    #     return data

    # validators = [UniqueTogetherValidator(queryset=Parties.objects.all(),fields=['customer_id', 'name'])]
    # def validate_name(value):
    #     if Parties.objects.filter(name__contains = self.name , city = self.city).exists():
    #         raise serializers.ValidationError("A party with this customer_id  already exists , try with other customer_id")

  
        
    
        

# USER SIGNUP SERIALIZER 

class UserSignupSerializer(serializers.Serializer):
    email = serializers.CharField(required = False)
    phone = serializers.CharField(required = False)
    party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all())
    first_name = serializers.CharField(required = False)
    last_name = serializers.CharField(required = False)
    display_name = serializers.CharField(required = False)
    supervisor = serializers.BooleanField(required = False)
    administrator = serializers.BooleanField(required = False)
    # profile_picture = serializers.ImageField(required = False , allow_empty_file=False , validators = [profile_img_validator])

    
    def create(self, validated_data):
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        display_name = validated_data.pop('display_name')
        # profile_picture = validated_data.pop('profile_picture')
        party = validated_data.pop('party')
        supervisor = validated_data.pop('supervisor')
        administrator = validated_data.pop('administrator')
    
        user = User.objects.create(phone = phone , email = email ,first_name = first_name ,  last_name =last_name,display_name = display_name , party = party,  is_supervisor = supervisor , is_administrator = administrator )
        user.save()
        return user
        

    def validate_email(self,value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("user with this email_id already exists")
        return value
        
    def validate_phone(self, attrs):
        if User.objects.filter(phone = attrs).exists():
            raise serializers.ValidationError("user with this phone number already exists")
        return attrs

    

    
# LOGIN SERIALIZER

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email","phone"]



# GET USER SERIALIZER

class GetUserSerilaizer(serializers.ModelSerializer):
    party = serializers.SlugRelatedField(read_only = True , slug_field= 'name')
    class Meta:
        model = User
        fields = [
            "id",
            "last_login",
            "phone",
            "email",
            "display_name",
            "first_name",
            "last_name",
            'party',
            'profile_img',
            'is_active',
            "is_supervisor",
            "is_administrator",
            "created_date",
        ]

    
# USER UPDATE SERIALIZER 

class UserUpdateSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'first_name',
            'last_name',
            'display_name',
            'profile_img',
            'party',
            'is_active',
            'is_supervisor',
            'is_administrator',
            'created_date',
            'last_login',
        ]




class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = '__all__'




class Countriesserializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'



class Actionserializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class Modelserializer(serializers.ModelSerializer):
    class Meta:
        model = Models
        fields = '__all__'



class signatureslistserializer(serializers.ModelSerializer):
    action = serializers.SlugRelatedField(read_only = True ,slug_field='desc')
    party = serializers.SlugRelatedField(read_only = True , slug_field= 'name')
    class Meta:
        model = signatures
        fields = [
            'id',
            'model',
            'action',
            'party',
            'sign_a',
            'sign_b',
            'sign_c'
        ]
    

class signaturecreateserializer(serializers.ModelSerializer):
    class Meta:
        model = signatures
        fields = '__all__'


class Userprocessserialzier(serializers.ModelSerializer):
    action = serializers.SlugRelatedField(read_only = True ,slug_field='desc')
    class Meta:
        model = userprocessauth
        fields = [
            'id',
            'user',
            'model',
            'action',
            'data_entry',
            'sign_a',
            'sign_b',
            'sign_c'
        ]



class userprocesscreateserializer(serializers.ModelSerializer):
    action = serializers.PrimaryKeyRelatedField(queryset=Action.objects.all())
    class Meta:
        model = userprocessauth
        fields = [
            'id',
            'model',
            'action',
            'user',
            'data_entry',
            'sign_a',
            'sign_b',
            'sign_c'
        ]





# UPDATED COUNTERPARTY SERIALIZER 12/9/22


class CounterpartyCreateSerializer(serializers.ModelSerializer):

    country_code = serializers.SlugRelatedField(read_only=True, slug_field='country')
    base_currency = serializers.SlugRelatedField(read_only=True, slug_field='description')
    # limit = serializers.SerializerMethodField()
    # max_Invoice_Amount = serializers.SerializerMethodField()
    # grace_period = serializers.SerializerMethodField()
    # Interest_Rate_Type = serializers.SerializerMethodField()
    # Margin = serializers.SerializerMethodField()
    # expiry_Date = serializers.SerializerMethodField()
    # max_invoice_pct = serializers.SerializerMethodField()
    # max_tenor = serializers.SerializerMethodField()
    # interest_type = serializers.SerializerMethodField()
    # user_detail = serializers.SerializerMethodField()
    buyer_details = serializers.SerializerMethodField()
    pairings_details = serializers.SerializerMethodField()
    wf_item_id = serializers.SerializerMethodField()

    class Meta:
        model = CounterParty
        fields = [
            'id',
            'name',
            'customer_id',
            'address',
            'onboarding',
            'city',
            'base_currency',
            'country_code',
            'email',
            'mobile',
            'gst_no',
            'pan_no',
            # 'user_detail',
            'wf_item_id',
            'buyer_details',
            'pairings_details'
        ]

    # def get_user_detail(self,obj):
    #     try:
    #         user_Data = User.objects.filter(party__name__contains = obj.name).first()
    #         return {"user_email": user_Data.email, "user_phone": user_Data.phone}
    #     except:
    #         return None
    def get_wf_item_id(self,obj):
        try:
            return obj.workflowitems.id
        except: pass

    def get_buyer_details(self,obj):
        try:
            return {"buyer_id" : obj.pairings.program_id.party.id , 
            "buyer_name" : obj.pairings.program_id.party.name , 
            "buyer_address" : obj.pairings.program_id.party.address_line_1 ,
            "program_type" : obj.pairings.program_id.program_type }
        except:
            pass
    

    def get_pairings_details(self,obj):
        try:
            pair = Pairings.objects.filter(id = obj.pairings.id).values()
            return {"pairing":pair}
        except:
            return None



class CounterpartyUpdateSerializer(serializers.Serializer):

    ON_BOARDING_STATUS = [
    ('DRAFT', 'DRAFT'),
    ('SENT_TO_BANK','SENT_TO_BANK'),
    ('SENT_TO_CUSTOMER','SENT_TO_CUSTOMER'),
    ('COMPLETE','COMPLETE'),
    ]

    onboarding = serializers.ChoiceField( choices = ON_BOARDING_STATUS , required = False)
    gst_no = serializers.CharField()
    pan_no = serializers.CharField()

    def update(self, instance, validated_data):
            # instance.name = validated_data.get('name', instance.name)
            # instance.address = validated_data.get('address', instance.address)
            # instance.city = validated_data.get('city', instance.city)
            # instance.country = validated_data.get('country', instance.country)
            # instance.email = validated_data.get('email', instance.email)
            # instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.onboarding = validated_data.get('onboarding', instance.onboarding)
        instance.gst_no = validated_data.get('gst_no', instance.gst_no)
        instance.pan_no = validated_data.get('pan_no', instance.pan_no)
        instance.save()
        return instance



class PartyStatusUpdateserializer(serializers.Serializer):
    STATUS_CHOICES = [
    ('NONE','NONE'),
    ('NEW','NEW'),
    ('IN_PROGRESS','IN_PROGRESS'),
    ('ONBOARDED','ONBOARDED'),
    ('DEACTIVATED','DEACTIVATED'),
    ]
    status = serializers.ChoiceField(choices = STATUS_CHOICES)
    

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)   
        instance.save()
        return instance



# UPDATED CHAT_USER LIST API # 23-9-2022

class ChatUsersSerializer(serializers.ModelSerializer):
    chat_users = serializers.SerializerMethodField()
    party_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'party',
            'party_name',
            'is_active',
            'chat_users'
        ]

    def get_party_name(self,obj):
        return obj.party.name

    def get_chat_users(self,obj):
        base_list = []
        base_list_2 = []
        bank = Parties.objects.filter(party_type = "BANK").values('name')
        for iters in bank:
            data = {"bank_name" : iters['name'] , 'users' : list(User.objects.filter(party__name = iters["name"]).values_list('email',flat = True))} 
            base_list_2.append(data)
        try:
            if obj.party.party_type == "SELLER" :
                # counterparty -> buyers
                pairings = Pairings.objects.filter(counterparty_id__name = obj.party.name ).values('program_id__party__name')
                # # buyer_user = User.objects.filter(party__name = pairings.program_id.party.name).values('party__name','email','is_active')
                # # Users = User.objects.filter(party__name = pairings.counterparty_id).exclude(id = obj.id).values('party__name','email','is_active')
                for users in pairings:
                    data = {"party_name" : users['program_id__party__name'] ,'users' : list(User.objects.filter(party__name = users['program_id__party__name']).values_list('email',flat = True))}
                    base_list.append(data)
                return {"buyer_user" : base_list , "bank_user" : base_list_2}
            else:
                # buyers -> counterparty
                program = Programs.objects.get(party = obj.party)
                pairings = Pairings.objects.filter(program_id = program.id ).values('counterparty_id__name')
                for users in pairings:        
                    # Users = User.objects.filter(party__name = users["counterparty_id__name"]).values('party__name','email','is_active') 
                    data = {"party_name" : users['counterparty_id__name'] , 'users' : list(User.objects.filter(party__name = users["counterparty_id__name"]).values_list('email',flat = True))} 
                    base_list.append(data)
                return {"counterparty_users" : base_list , "bank_user" : base_list_2}
        except:
            return None



class PartieSearchserializer(serializers.ModelSerializer):
    class Meta:
        model = Parties
        fields = ['account_number', 'customer_id']




#  MISC FOR SIGNUPO_PROCESS


class SignupProcessSerializer(serializers.Serializer):
    account_number = serializers.CharField(required = False )
    customer_id = serializers.CharField(required = False)
    name = serializers.CharField()
    city = serializers.CharField()
    currency = serializers.PrimaryKeyRelatedField(queryset = Currencies.objects.all())
    country = serializers.PrimaryKeyRelatedField(queryset = Countries.objects.all())
    zipcode = serializers.CharField()
    party = serializers.PrimaryKeyRelatedField(queryset = Parties.objects.all().filter(party_type = "BUYER") , required = False )
    address = serializers.CharField()
    state = serializers.CharField()
    email = serializers.EmailField(required = False)
    phone = serializers.IntegerField(required =  False)

    def create(self , validated_data):
        account_number = validated_data.pop('account_number')
        customer_id = validated_data.pop('customer_id')
        name = validated_data.pop('name')
        city = validated_data.pop('city')
        country = validated_data.pop('country')
        currency = validated_data.pop('currency')
        zipcode = validated_data.pop('zipcode')
        party = validated_data.pop('party')
        address = validated_data.pop('address')
        state = validated_data.pop('state')
        email = validated_data.pop('email')
        phone = validated_data.pop('phone')

        signupprocess.objects.update_or_create(account_number = account_number, address = address, state = state ,
                    customer_id = customer_id , name = name, currency = currency , country = country ,
                    zipcode = zipcode  , city = city )
        obj , created = Parties.objects.get_or_create( name = name , city = city.lower() , account_number = account_number  , customer_id = customer_id ,
        defaults = { 'base_currency' : currency ,'address_line_1' : address , 'address_line_2' : address, 'city' : city , 'state' : state , 'zipcode' : zipcode, 'country_code' : country , 'party_type' : "BUYER" })
        User.objects.create(phone = phone , party = obj , email = email)
        # creating a pairing 
