from django.contrib.auth import get_user_model

from transaction.models import Pairings
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
	    }

    # validators = [UniqueTogetherValidator(queryset=Parties.objects.all(),fields=['customer_id', 'name'])]
    # def validate_customer_id(self,value):
    #     if Parties.objects.filter(customer_id = value).exists():
    #         raise serializers.ValidationError("A party with this customer_id  already exists , try with other customer_id")
    #     return value

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

    customer_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    country = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    mobile = serializers.CharField(required=True)
    onboarding = serializers.ChoiceField(choices=choices)
    gst_no = serializers.CharField(required=True)
    pan_no = serializers.CharField(required=True)

    def create(self, validated_data):

        customer_id = validated_data.pop('customer_id')
        name = validated_data.pop('name')
        address = validated_data.pop('address')
        city = validated_data.pop('city')
        country = validated_data.pop('country')
        email = validated_data.pop('email')
        mobile = validated_data.pop('mobile')
        onboarding = validated_data.pop('onboarding')
        gst_no = validated_data.pop('gst_no')
        pan_no = validated_data.pop('pan_no')

        counter_party = CounterParty.objects.create(id=customer_id,
                                                    name=name,
                                                    address=address,
                                                    city=city,
                                                    country=country,
                                                    email=email,
                                                    mobile=mobile,
                                                    onboarding=onboarding,
                                                    gst_no=gst_no,
                                                    pan_no=pan_no)

        party = Parties.objects.create(
            customer_id=customer_id, name=name, address_line_1=address, city=city, party_type="OTHER")
        # need to update status for parties 
        party.save()
        counter_party.save()

        return counter_party

    def validate_name(self, value):
        if Parties.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Party with same name already exists.")
        return value



class CounterpartyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CounterParty
        fields = ['id', 'name', 'address', 'city', 'country',
                  'email', 'mobile', 'onboarding', 'gst_no', 'pan_no']
        read_only_fields = ['id']

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.address = validated_data.get(
                'address', instance.address)
            instance.city = validated_data.get('city', instance.city)
            instance.country = validated_data.get(
                'country', instance.country)
            instance.email = validated_data.get('email', instance.email)
            instance.mobile = validated_data.get(
                'mobile', instance.mobile)
            instance.onboarding = validated_data.get(
                'onboarding', instance.onboarding)
            instance.gst_no = validated_data.get('gst_no', instance.gst_no)
            instance.pan_no = validated_data.get('pan_no', instance.pan_no)

            instance.save()
            return instance
