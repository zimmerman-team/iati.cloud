from collections import OrderedDict
from api.renderers import PaginatedCSVRenderer


class ActivityCSVRenderer(PaginatedCSVRenderer):
    # mapping of Serializer field name -> CSV column label
    labels = OrderedDict([
        ('iati_identifier', 'iati-identifier'),
        ('hierarchy', 'hierarchy'),
        ('last_updated_datetime', 'last-updated-datetime'),
        ('default_lang', 'default-language'),
        ('reporting_org', 'reporting-org'),
        ('reporting_org_ref', 'reporting-org-ref'),
        ('reporting-org_type', 'reporting-org-type'),
        ('reporting-org_type_code', 'reporting-org-type-code'),
        ('title', 'title'),
        ('description', 'description'),
        ('activity_status_code', 'activity-status-code'),
        ('actual_end', 'end-actual'),
        ('actual_start', 'start-actual'),
        ('planned_end', 'end-planned'),
        ('planned_start', 'start-planned'),

        ('participating-org (Accountable)', 'participating-org (Accountable)'),
        ('participating-org-ref (Accountable)', 'participating-org-ref (Accountable)'),
        ('participating-org-type (Accountable)', 'participating-org-type (Accountable)'),
        ('participating-org-type-code (Accountable)', 'participating-org-type-code (Accountable)'),
        ('participating-org (Funding)', 'participating-org (Funding)'),
        ('participating-org-ref (Funding)', 'participating-org-ref (Funding)'),
        ('participating-org-type (Funding)', 'participating-org-type (Funding)'),
        ('participating-org-type-code (Funding)', 'participating-org-type-code (Funding)'),
        ('participating-org (Extending)', 'participating-org (Extending)'),
        ('participating-org-ref (Extending)', 'participating-org-ref (Extending)'),
        ('participating-org-type (Extending)', 'participating-org-type (Extending)'),
        ('participating-org-type-code (Extending)', 'participating-org-type-code (Extending)'),
        ('participating-org (Implementing)', 'participating-org (Implementing)'),
        ('participating-org-ref (Implementing)', 'participating-org-ref (Implementing)'),
        ('participating-org-type (Implementing)', 'participating-org-type (Implementing)'),
        ('participating-org-type-code (Implementing)', 'participating-org-type-code (Implementing)'),

        ('recipient_country_code', 'recipient-country-code'),
        ('recipient_country_description', 'recipient-country'),
        ('recipient_country_percentage', 'recipient-country-percentage'),

        ('recipient_region_code', 'recipient-region-code'),
        ('recipient_region_description', 'recipient-region'),
        ('recipient_region_percentage', 'recipient-region-percentage'),

        ('sector_code', 'sector-code'),
        ('sector_description', 'sector'),
        ('sector_percentage', 'sector-percentage'),
        ('sector_vocabulary', 'sector-vocabulary'),
        ('sector_vocabulary_code', 'sector-vocabulary-code'),

        ('collaboration_type_code', 'collaboration-type-code'),
        ('default_aid_type_code', 'default-aid-type-code'),
        ('default_finance_type_code', 'default-finance-type-code'),
        ('default_flow_type_code', 'default-flow-type-code'),
        ('default_tied_status_code', 'default-tied-status-code'),

        ('default_currency', 'default-currency'),
        ('currency', 'currency'),
        # ('total-Commitment', 'total-Commitment'),
        # ('total-Disbursement', 'total-Disbursement'),
        # ('total-Expenditure', 'total-Expenditure'),
        # ('total-Incoming Funds', 'total-Incoming Funds'),
        # ('total-Interest Repayment', 'total-Interest Repayment'),
        # ('total-Loan Repayment', 'total-Loan Repayment'),
        # ('total-Reimbursement', 'total-Reimbursement'),
    ])

    header = labels.keys()
