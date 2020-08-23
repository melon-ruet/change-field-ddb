import uuid

import pynamodb.attributes


# UUID  Attribute will use as Dynamo hash key
class UUIDAttribute(pynamodb.attributes.UnicodeAttribute):

    def serialize(self, value):
        return super().serialize(str(value))

    def deserialize(self, value):
        return uuid.UUID(super().deserialize(value))


# Add custom attribute to serialize and deserialize data
class ResultAttribute(pynamodb.attributes.MapAttribute):

    @classmethod
    def is_raw(cls):
        # Set to use as AttributeContainer
        # https://pynamodb.readthedocs.io/en/latest/api.html#pynamodb.attributes.MapAttribute
        return True

    @staticmethod
    def _parse_value(values):
        return {
            f'semester {idx+1}': val for idx, val in enumerate(values)
        }

    def serialize(self, values):
        # Convert python list to native pynamo
        if isinstance(values, (list, tuple)):
            values = self._parse_value(values)
        return super().serialize(values)

    def get_value(self, value):
        try:
            # Convert from
            # {'L': [{'N': '3.75'}, {'N': '3.17'}]}
            # to
            # {'M': {'semester 1': {'N': '3.75'}, 'semester 2': {'N': '3.17'}}}
            value = {'M': self._parse_value(value['L'])}
        except (KeyError, TypeError):
            pass
        return super().get_value(value)
