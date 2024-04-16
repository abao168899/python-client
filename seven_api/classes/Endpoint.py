from seven_api.classes.ExtendedEnum import ExtendedEnum


class Endpoint(ExtendedEnum):
    ANALYTICS = 'analytics'
    BALANCE = 'balance'
    CONTACTS = 'contacts'
    GROUPS = 'groups'
    HOOKS = 'hooks'
    JOURNAL = 'journal'
    LOOKUP = 'lookup'
    PRICING = 'pricing'
    RCS = 'rcs'
    RCS_EVENTS = f'{RCS}/events'
    RCS_MESSAGES = f'{RCS}/messages'
    SMS = 'sms'
    STATUS = 'status'
    SUBACCOUNTS = 'subaccounts'
    VALIDATE_FOR_VOICE = 'validate_for_voice'
    VOICE = 'voice'
