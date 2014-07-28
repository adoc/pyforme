import formencode
import forme.validators.crm

class ContactSchema(formencode.schema.Schema):
    """Schema mixin for common location address keys.
    """
    allow_extra_fields = True
    filter_extra_fields = True
    ignore_key_missing = False

    email1 = formencode.validators.Email(resolve_domain=True, not_empty=True)
    email2 = formencode.validators.Email(resolve_domain=True, not_empty=False)
    address1 = formencode.validators.UnicodeString(min=4, max=100,
                                                   not_empty=True)
    address2 = formencode.validators.UnicodeString(min=1, max=32,
                                                   not_empty=False)
    city = formencode.validators.UnicodeString(min=3, max=64, not_empty=True)
    state = formencode.validators.String(min=2, max=4, not_empty=True)
    zipcode = formencode.validators.Int(min=10000, max=99999, not_empty=True)
    phone1 = forme.validators.crm.PhoneValidator(min=10, max=16,
                                                 not_empty=True)
    phone2 = forme.validators.crm.PhoneValidator(min=10, max=16,
                                                 not_empty=False)
