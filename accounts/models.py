from django.db import models
from django.contrib.auth.models import (
    BaseUserManager , 
    AbstractBaseUser ,
    PermissionsMixin
)
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from .file_path import profile_img_path




# CURRENCIES      

class Currencies(models.Model):
    iso = models.IntegerField()
    description = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        return super(Currencies, self).save(*args, **kwargs)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Currency"

# COUNTRIES

class Countries(models.Model):
    country = models.CharField(max_length=100,null=True,blank=True)
    dial_code = models.IntegerField()

    def save(self, *args, **kwargs):
        self.country = self.country.upper()
        return super(Countries,self).save(*args, **kwargs)

    def __str__(self):
        return self.country
    
    class Meta:
        verbose_name_plural = "Country"



# BANK 

class Banks(models.Model):
    name = models.CharField(max_length=40,null=True,blank=True)
    address_line_1 = models.CharField(max_length=30)
    address_line_2 = models.CharField(max_length=20)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    zipcode = models.CharField(max_length=6)
    country_code = models.ForeignKey(Countries,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s - %s"%(self.name , self.country_code)

    class Meta:
        verbose_name_plural = "Bank"


# PARTIES 

class Parties(models.Model):
    
    party_type_choices = [
    ('CUSTOMER','CUSTOMER'),
    ('BANK','BANK'),
    ('OTHER','OTHER'),
    ('SELLER','SELLER'),
    ('BUYER','BUYER'),
    ('OTHER','OTHER'),
    ]

    STATUS_CHOICES = [
    ('NONE','NONE'),
    ('NEW','NEW'),
    ('IN_PROGRESS','IN_PROGRESS'),
    ('ONBOARDED','ONBOARDED'),
    ('DEACTIVATED','DEACTIVATED'),
    ]

    account_number = models.BigIntegerField(blank=True, null=True)
    customer_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    base_currency  = models.ForeignKey(Currencies,on_delete=models.CASCADE , blank=True, null=True)
    address_line_1 = models.CharField(max_length=35 , blank=True, null=True)
    address_line_2 = models.CharField(max_length=35 , blank=True, null=True)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    zipcode = models.CharField(max_length=6 , blank=True, null=True)
    country_code = models.ForeignKey(Countries,on_delete=models.DO_NOTHING , blank=True, null=True)
    onboarded = models.BooleanField(default=False)
    party_type = models.CharField(choices = party_type_choices , max_length=25)
    status = models.CharField(choices = STATUS_CHOICES ,  max_length=255 )

    class Meta:
        verbose_name_plural = "Party"
        ordering = ['id']
        unique_together = (('name', 'city'))

    def save(self, *args, **kwargs):
        self.name , self.city = self.name.upper() , self.city.lower()
        return super(Parties, self).save(*args, **kwargs)

    def __str__(self):
        return "%s   (%s)"%(self.name , self.party_type)

    

    # @property
    # def party_id(self):
    #     return self.id

    


# COUNTERPARTY 

class CounterParty(models.Model):

    choices = [
        ('DRAFT', 'DRAFT'),
        ('SENT TO BANK', 'SENT TO BANK'),
        ('SENT TO COUNTERPARTY', 'SENT TO COUNTERPARTY'),
        ('COMPLETED', 'COMPLETED'),
        ('REJECTED', 'REJECTED'),
    ]

    customer_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country_code = models.ForeignKey(Countries,on_delete=models.DO_NOTHING , blank=True, null=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    onboarding = models.CharField(choices=choices, max_length=25 , blank=True, null=True)
    gst_no = models.CharField(max_length=18 , blank=True, null=True)
    pan_no = models.CharField(max_length=18 , blank=True, null=True)
    
    # class Meta:
    #     pass

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name , self.city = self.name.upper() , self.city.lower()
        return super(CounterParty, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "CounterParty"
        ordering = ['id']
        unique_together = ('name', 'city')

    

    # def random_generator(self):
    #     pass 


    





# PARTY ACCOUNTS_CONFIG

class Partyaccounts(models.Model):
    account_number = models.CharField(max_length=34)
    currency = models.ForeignKey(Currencies,on_delete=models.DO_NOTHING)
    party_id = models.ForeignKey(Parties,on_delete=models.DO_NOTHING)
    account_with_bank = models.ForeignKey(Banks,on_delete=models.DO_NOTHING)

    def __str__(self):
        return "%s related with party  %s"%(self.account_number , self.party_id)

    class Meta:
        verbose_name_plural = "PartyAccounts"



# CUSTOM USER MODEL SETUP  ( PHONE / EMAIL )  - AUTHENTICATION

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        is_active = kwargs.pop("is_active", False)
        is_supervisor = kwargs.pop("is_supervisor", False)
        is_administrator = kwargs.pop("is_administrator", False)
        is_master_admin = kwargs.pop('is_master_admin',False)
        user = self.model(
            email=email,
            is_active=is_active,
            is_supervisor=is_supervisor,
            is_administrator=is_administrator,
            is_master_admin=is_master_admin,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email,
            password,
            is_active=True,
            is_supervisor=True,
            is_administrator=True,
            is_master_admin=True,
            **extra_fields
        )


# MY USER MODEL -- updated master

class User(AbstractBaseUser,PermissionsMixin):
    phone = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)
    party = models.ForeignKey(Parties,on_delete=models.CASCADE,blank=True, null=True)
    counterparty = models.ForeignKey(CounterParty,on_delete=models.CASCADE,blank=True, null=True)
    first_name = models.CharField(max_length=100 , blank=True, null=True)
    last_name = models.CharField(max_length=100 , blank=True, null=True)
    display_name = models.CharField(max_length=255 , blank=True, null=True)
    is_active = models.BooleanField(default=True, blank = False)
    is_supervisor = models.BooleanField(default=False)
    profile_img = models.ImageField(upload_to = profile_img_path , blank = True ,  null = True)
    is_administrator = models.BooleanField(default=False)
    is_master_admin = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    # is_supervisor -> who supervises all the signatures activities for his related party
    
    # is_administrator -> a party's administrator who can create signatures and actions for his own party 
    # is_administrator == True  -> can login in admin_panel with only minimal permissions
    @property
    def is_staff(self):
        return self.is_administrator

    # is_master_admin is the user who maintains all the permissions and  admin-panel ( belongs to bank )
    @property
    def is_superuser(self):
        return self.is_master_admin

    ## for admin panel showing profile_img
    def profile_tags(self):
        if self.profile_img :
            return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.profile_img))
        else:
            return 'No image found'

    profile_tags.short_description = 'Image'

    class Meta:
        ordering = ['id']
        unique_together = ('phone', 'email')

    



# OTP MODELS 

class PhoneOTP(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=16)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return "%s - %s"%(self.phone , self.otp)



# MODELS 

class Models(models.Model):
    desc = models.CharField(max_length=155)
    api_route = models.CharField(max_length=155)

    class Meta:
        verbose_name_plural = "Model"


# ACTIONS

class Action(models.Model):
    desc = models.CharField(max_length=55)
    bank = models.BooleanField(blank=True, null=True,default=False)
    customer = models.BooleanField(default=False , blank=True, null=True)

    def save(self, *args, **kwargs):
        self.desc = self.desc.upper()
        return super(Action, self).save(*args, **kwargs)

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name_plural = "Action"
    

# SIGNATURE LEVELS

class signatures(models.Model):
    model = models.CharField(max_length=55)
    action = models.ForeignKey(Action,on_delete=models.DO_NOTHING)
    party = models.ForeignKey(Parties,on_delete=models.CASCADE)
    sign_a = models.BooleanField(default=False , blank=True, null=True)
    sign_b = models.BooleanField(default=False,blank=True, null=True)
    sign_c = models.BooleanField(default=False , blank=True, null=True)

    def save(self, *args, **kwargs):
        self.model = self.model.upper()
        return super(signatures, self).save(*args, **kwargs)

    def __str__(self):
        return "%s -> %s of action -> %s "%(self.model , self.party , self.action)
    
    class Meta:
        verbose_name_plural = "Signatures"
        indexes = [
            models.Index(fields=['id',]),
            models.Index(fields=['model',]),
            models.Index(fields=['action',]),
            models.Index(fields=['party',]),
        ]
        unique_together = ('model', 'action','party')       

        

    

# USER PROCESS AUTH

class userprocessauth(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    model = models.CharField(max_length=55)
    action = models.ForeignKey(Action,on_delete=models.DO_NOTHING)
    data_entry = models.BooleanField(default=False,blank=True, null=True)
    sign_a = models.BooleanField(default=False,blank=True, null=True)
    sign_b = models.BooleanField(default=False,blank=True, null=True)
    sign_c = models.BooleanField(default=False,blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.model = self.model.upper()
        return super(userprocessauth, self).save(*args, **kwargs)

    def __str__(self):
        return "%s -> %s -> %s"%(self.model , self.action,self.user)

    class Meta:
        verbose_name_plural = "userprocessauth"
        unique_together = ('action', 'user','model')





#  MISC FOR SIGNUP_PROCESS ( 3RD PARTY ) MISC


class signupprocess(models.Model):
    
    party_type_choices = [
    ('BUYER','BUYER'),
    ]

    STATUS_CHOICES = [
    ('NONE','NONE'),
    ('NEW','NEW'),
    ('IN_PROGRESS','IN_PROGRESS'),
    ('ONBOARDED','ONBOARDED'),
    ('DEACTIVATED','DEACTIVATED'),
    ]

    account_number = models.BigIntegerField(blank=True, null=True)
    customer_id = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    base_currency  = models.ForeignKey(Currencies,on_delete=models.CASCADE , blank=True, null=True)
    address_line_1 = models.CharField(max_length=35 , blank=True, null=True)
    address_line_2 = models.CharField(max_length=35 , blank=True, null=True)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length = 255)
    city = models.CharField(max_length=35)
    state = models.CharField(max_length=35)
    zipcode = models.CharField(max_length=6 , blank=True, null=True)
    country_code = models.ForeignKey(Countries,on_delete=models.DO_NOTHING , blank=True, null=True)
    onboarded = models.BooleanField(default=False)
    party_type = models.CharField(default = "BUYER" , max_length=25)
    status = models.CharField(choices = STATUS_CHOICES ,  max_length=255 )