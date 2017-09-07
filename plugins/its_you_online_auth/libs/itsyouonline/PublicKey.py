"""
Auto-generated class for PublicKey
"""
from plugins.its_you_online_auth.libs.itsyouonline import client_support
from .Label import Label


class PublicKey(object):
    """
    auto-generated. don't touch.
    """

    @staticmethod
    def create(label, publickey):
        """
        :type label: Label
        :type publickey: str
        :rtype: PublicKey
        """

        return PublicKey(
            label=label,
            publickey=publickey,
        )

    def __init__(self, json=None, **kwargs):
        if json is None and not kwargs:
            raise ValueError('No data or kwargs present')

        class_name = 'PublicKey'
        create_error = '{cls}: unable to create {prop} from value: {val}: {err}'
        required_error = '{cls}: missing required property {prop}'

        data = json or kwargs

        property_name = 'label'
        val = data.get(property_name)
        if val is not None:
            datatypes = [Label]
            try:
                self.label = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

        property_name = 'publickey'
        val = data.get(property_name)
        if val is not None:
            datatypes = [str]
            try:
                self.publickey = client_support.val_factory(val, datatypes)
            except ValueError as err:
                raise ValueError(create_error.format(cls=class_name, prop=property_name, val=val, err=err))
        else:
            raise ValueError(required_error.format(cls=class_name, prop=property_name))

    def __str__(self):
        return self.as_json(indent=4)

    def as_json(self, indent=0):
        return client_support.to_json(self, indent=indent)

    def as_dict(self):
        return client_support.to_dict(self)