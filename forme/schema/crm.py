import formencode
import datetime
import forme.validators.crm


def contact_schema(partial=False):
    class ContactSchema(formencode.schema.Schema):
        """Schema mixin for common location address keys.
        """
        allow_extra_fields = True
        filter_extra_fields = True
        ignore_key_missing = False

        email1 = formencode.validators.Email(resolve_domain=True,
                                             not_empty=True)
        email2 = formencode.validators.Email(resolve_domain=True,
                                             not_empty=False,if_missing=None)
        address1 = formencode.validators.UnicodeString(min=4, max=100,
                                                       not_empty=True)
        address2 = formencode.validators.UnicodeString(min=1, max=32,
                                                       not_empty=False,
                                                       if_missing=None)
        city = formencode.validators.UnicodeString(min=3, max=64,
                                                   not_empty=True)
        state = formencode.validators.String(min=2, max=4, not_empty=True)
        zipcode = formencode.validators.Int(min=10000, max=99999,
                                            not_empty=True)
        phone1 = forme.validators.crm.PhoneValidator(min=10, max=16,
                                                     not_empty=True)
        phone2 = forme.validators.crm.PhoneValidator(min=10, max=16,
                                                     not_empty=False,
                                                     if_missing=None)

    if partial is True:
        ContactSchema.ignore_key_missing = True
        ContactSchema.fields['email1'].not_empty = False
        ContactSchema.fields['address1'].not_empty = False
        ContactSchema.fields['city'].not_empty = False
        ContactSchema.fields['state'].not_empty = False
        ContactSchema.fields['zipcode'].not_empty = False
        ContactSchema.fields['phone1'].not_empty = False

    return ContactSchema

ContactSchema = contact_schema()


def vehicle_schema(partial=False):
    this_year = datetime.datetime.now().year
    class VehicleSchema(formencode.schema.Schema):
        """
        """
        allow_extra_fields = True
        filter_extra_fields = True
        ignore_key_missing = False

        year = formencode.validators.Int(min=this_year-100, max=this_year+1,
                                         not_empty=True)
        make = formencode.validators.UnicodeString(min=3, max=32, not_empty=True)
        model = formencode.validators.UnicodeString(min=1, max=32, not_empty=True)
        vin = formencode.validators.String(min=17, max=17, not_empty=True)

    if partial is True:
        VehicleSchema.ignore_key_missing = True
        VehicleSchema.fields['year'].not_empty = False
        VehicleSchema.fields['make'].not_empty = False
        VehicleSchema.fields['model'].not_empty = False
        VehicleSchema.fields['vin'].not_empty = False

    return VehicleSchema
VehicleSchema = vehicle_schema()