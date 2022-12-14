# Generated by Django 3.2.5 on 2022-10-05 15:10

import accounts.file_path
import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterestChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=55)),
            ],
            options={
                'verbose_name_plural': 'InterestChoice',
            },
        ),
        migrations.CreateModel(
            name='InterestRateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=55)),
            ],
            options={
                'verbose_name_plural': 'InterestRateType',
            },
        ),
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_type', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_no', models.CharField(blank=True, max_length=10, null=True)),
                ('issue_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('due_date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('funding_req_type', models.CharField(blank=True, choices=[('AUTOMATIC', 'AUTOMATIC'), ('ON_REQUEST', 'ON_REQUEST')], default=None, max_length=15, null=True)),
                ('interest_rate', models.DecimalField(blank=True, decimal_places=1, max_digits=8, null=True)),
                ('financed_amount', models.DecimalField(blank=True, decimal_places=1, max_digits=8, null=True)),
                ('bank_loan_id', models.CharField(blank=True, max_length=55, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('finance_currency_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='financedinvoicecurrency', to='accounts.currencies')),
                ('invoice_currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invoicecurrencytype', to='accounts.currencies')),
            ],
            options={
                'verbose_name_plural': 'Invoice',
            },
        ),
        migrations.CreateModel(
            name='Invoiceuploads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_type', models.CharField(choices=[('*', '*'), ('APF', 'APF'), ('RF', 'RF'), ('DF', 'DF')], default='*', max_length=15)),
                ('invoices', models.JSONField()),
                ('is_finished', models.BooleanField(blank=True, default=None, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Invoiceupload',
            },
        ),
        migrations.CreateModel(
            name='Programs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_type', models.CharField(choices=[('ALL', 'ALL'), ('APF', 'APF'), ('RF', 'RF'), ('DF', 'DF')], default='*', max_length=10)),
                ('finance_request_type', models.CharField(blank=True, choices=[('AUTOMATIC', 'AUTOMATIC'), ('ON_REQUEST', 'ON_REQUEST')], default=None, max_length=15, null=True)),
                ('limit_currency', models.CharField(blank=True, max_length=3, null=True)),
                ('total_limit_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('finance_currency', models.CharField(blank=True, max_length=3, null=True)),
                ('settlement_currency', models.CharField(blank=True, max_length=3, null=True)),
                ('expiry_date', models.DateField(default=datetime.date.today)),
                ('max_finance_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('max_invoice_age_for_funding', models.IntegerField(blank=True, null=True)),
                ('max_age_for_repayment', models.IntegerField(blank=True, null=True)),
                ('minimum_period', models.IntegerField(blank=True, null=True)),
                ('maximum_period', models.IntegerField(blank=True, null=True)),
                ('maximum_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('minimum_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('financed_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('balance_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('grace_period', models.IntegerField(blank=True, null=True)),
                ('interest_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('margin', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=155, null=True)),
                ('is_locked', models.BooleanField(blank=True, default=None, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('interest_rate_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transaction.interestratetype')),
                ('interest_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transaction.interestchoice')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.parties')),
            ],
            options={
                'verbose_name_plural': 'Program',
            },
        ),
        migrations.CreateModel(
            name='Transitionpartytype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=55)),
            ],
            options={
                'verbose_name_plural': 'Transitionpartytype',
            },
        ),
        migrations.CreateModel(
            name='workflowitems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('initial_state', models.CharField(default='DRAFT', max_length=50)),
                ('interim_state', models.CharField(default='DRAFT', max_length=50)),
                ('final_state', models.CharField(default='DRAFT', max_length=50)),
                ('next_available_transitions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default=None, max_length=500, null=True), blank=True, default=None, null=True, size=None)),
                ('action', models.CharField(default='SAVE', max_length=25)),
                ('subaction', models.CharField(blank=True, max_length=55, null=True)),
                ('previous_action', models.CharField(blank=True, max_length=55, null=True)),
                ('type', models.CharField(max_length=55)),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
                ('is_read', models.BooleanField(blank=True, default=True, null=True)),
                ('counterparty', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.counterparty')),
                ('current_from_party', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='from_party', to='accounts.parties')),
                ('current_to_party', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='to_party', to='accounts.parties')),
                ('invoice', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.invoices')),
                ('program', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.programs')),
                ('uploads', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.invoiceuploads')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customername', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Workflowitem',
            },
        ),
        migrations.CreateModel(
            name='workevents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_state', models.CharField(default='DRAFT', max_length=50)),
                ('action', models.CharField(default='SAVE', max_length=25)),
                ('subaction', models.CharField(blank=True, max_length=55, null=True)),
                ('to_state', models.CharField(default='DRAFT', max_length=50)),
                ('interim_state', models.CharField(default='DRAFT', max_length=50)),
                ('record_datas', models.JSONField(blank=True, null=True)),
                ('end', models.CharField(blank=True, max_length=55, null=True)),
                ('is_read', models.BooleanField(blank=True, default=True, null=True)),
                ('final', models.CharField(blank=True, max_length=55, null=True)),
                ('c_final', models.CharField(blank=True, max_length=55, null=True)),
                ('comments', models.CharField(blank=True, max_length=500, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=55)),
                ('event_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_user', to=settings.AUTH_USER_MODEL)),
                ('from_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_we_party', to='accounts.parties')),
                ('to_party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_wf_party', to='accounts.parties')),
                ('workitems', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflowevent', to='transaction.workflowitems')),
            ],
            options={
                'verbose_name_plural': 'WorkEvent',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Pairings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finance_request', models.CharField(blank=True, choices=[('AUTOMATIC', 'AUTOMATIC'), ('ON_REQUEST', 'ON_REQUEST')], default=None, max_length=15, null=True)),
                ('total_limit', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('expiry_date', models.DateField(default=datetime.date.today)),
                ('max_finance_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('max_invoice_age_for_funding', models.IntegerField(blank=True, null=True)),
                ('max_age_for_repayment', models.IntegerField(blank=True, null=True)),
                ('minimum_period', models.IntegerField(blank=True, null=True)),
                ('maximum_period', models.IntegerField(blank=True, null=True)),
                ('minimum_amount_currency', models.CharField(blank=True, max_length=3, null=True)),
                ('minimum_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('maximum_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('financed_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('balance_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('grace_period', models.IntegerField(blank=True, null=True)),
                ('interest_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('margin', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('counterparty_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.counterparty')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pairingscurrency', to='accounts.currencies')),
                ('finance_currency_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='financedcurrency', to='accounts.currencies')),
                ('interest_rate_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transaction.interestratetype')),
                ('interest_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='transaction.interestchoice')),
                ('program_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.programs')),
                ('settlement_currency_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.currencies')),
            ],
            options={
                'verbose_name_plural': 'Pairing',
            },
        ),
        migrations.AddField(
            model_name='invoices',
            name='pairing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='transaction.pairings'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='party',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.parties'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='settlement_currency_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.currencies'),
        ),
        migrations.CreateModel(
            name='FundingRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.IntegerField()),
                ('financed_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('balance_amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('due_date', models.DateField(default=datetime.date.today)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transaction.programs')),
            ],
            options={
                'verbose_name_plural': 'FundingRequest',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.FileField(upload_to=accounts.file_path.manage_scf_attachments)),
                ('invoice_upload', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.invoiceuploads')),
                ('pairing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.pairings')),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transaction.programs')),
            ],
        ),
    ]
