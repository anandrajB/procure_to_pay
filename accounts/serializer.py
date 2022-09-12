from django.contrib.auth import get_user_model
from .models import (
    Action,
    Banks, 
    Countries,
    Currencies,
    Parties, 
    CounterParty, 
    PhoneOTP, 
    signatures, 
    userprocessauth,
    Models 
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
            'city',
            'base_currency',
            'state',
            'zipcode',
            'country_code',
            'party_type'
        ]


# PARTY SIGNUP SERIALIZERS

class PartiesSignupSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Parties
        fields = '__all__'
        extra_kwargs = {
		"address_line_1": {"required": False},
        "address_line_2": {"required": False},
        "city": {"required": False},
        "state": {"required": False},
        "zipcode": {"required": False},
	    }

    # validators = [UniqueTogetherValidator(queryset=Parties.objects.all(),fields=['customer_id', 'name'])]
    def validate_customer_id(self,value):
        if Parties.objects.filter(customer_id = value).exists():
            raise serializers.ValidationError("A party with this customer_id  already exists , try with other customer_id")
        return value

    def validate_name(self,value):
        if Parties.objects.filter(name__contains = value).exists():
            raise serializers.ValidationError("A party with this name already exists , try with other name")
        return value

    
        

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

    def validate_party(self, attrs):
        if Parties.objects.filter(party__iexact = attrs).exists():
            raise serializers.ValidationError("Party with this name already exists")
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


class CounterpartyCreateSerializer(serializers.Serializer):

    choices = [
        ('DRAFT', 'DRAFT'),
        ('SENT TO BANK', 'SENT TO BANK'),
        ('SENT TO COUNTERPARTY', 'SENT TO COUNTERPARTY'),
        ('COMPLETED', 'COMPLETED'),
        ('REJECTED', 'REJECTED'),
    ]

    c_id = serializers.CharField(required=True)
    c_name = serializers.CharField(required=True)
    c_address = serializers.CharField(required=True)
    c_city = serializers.CharField(required=True)
    c_country = serializers.CharField(required=True)
    c_email = serializers.EmailField(required=True)
    c_mobile = serializers.CharField(required=True)
    c_onboarding = serializers.ChoiceField(choices=choices)
    gst_no = serializers.CharField(required=True)
    pan_no = serializers.CharField(required=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):

        c_id = validated_data.pop('c_id')
        c_name = validated_data.pop('c_name')
        c_address = validated_data.pop('c_address')
        c_city = validated_data.pop('c_city')
        c_country = validated_data.pop('country')
        c_email = validated_data.pop('c_email')
        c_mobile = validated_data.pop('c_mobile')
        c_onboarding = validated_data.pop('c_onboarding')
        gst_no = validated_data.pop('gst_no')
        pan_no = validated_data.pop('pan_no')
        user = validated_data.pop('user')

        counter_party = CounterParty.objects.create(c_id=c_id,
                                                    c_name=c_name,
                                                    c_address=c_address,
                                                    c_city=c_city,
                                                    c_country=c_country,
                                                    c_email=c_email,
                                                    c_mobile=c_mobile,
                                                    c_onboarding=c_onboarding,
                                                    gst_no=gst_no,
                                                    pan_no=pan_no, user=user)

        party = Parties.objects.create(
            customer_id=c_id, name=c_name, address_line_1=c_address, city=c_city, party_type="OTHER", status="NEW")

        party.save()
        counter_party.save()

        return counter_party

    def validate_name(self, value):
        if Parties.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Party with same name already exists.")
        return value

# CounterParty Update Serializer


class CounterpartyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CounterParty
        fields = ['c_id', 'c_name', 'c_address', 'c_city', 'c_country',
                  'c_email', 'c_mobile', 'c_onboarding', 'gst_no', 'pan_no']
        read_only_fields = ['c_id']

        def update(self, instance, validated_data):
            instance.c_name = validated_data.get('c_name', instance.c_name)
            instance.c_address = validated_data.get(
                'c_address', instance.c_address)
            instance.c_city = validated_data.get('c_city', instance.c_city)
            instance.c_country = validated_data.get(
                'c_country', instance.c_country)
            instance.c_email = validated_data.get('c_email', instance.c_email)
            instance.c_mobile = validated_data.get(
                'c_mobile', instance.c_mobile)
            instance.c_onboarding = validated_data.get(
                'c_onboarding', instance.c_onboarding)
            instance.gst_no = validated_data.get('gst_no', instance.gst_no)
            instance.pan_no = validated_data.get('pan_no', instance.pan_no)

            instance.save()
            return instance
