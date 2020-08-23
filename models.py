import uuid

import pynamodb.models
import pynamodb.attributes

from attributes import UUIDAttribute, ResultAttribute


class ResultModel(pynamodb.models.Model):
    id = UUIDAttribute(hash_key=True, default=uuid.uuid4)
    result = ResultAttribute()

    class Meta:
        table_name = "test-ddb-table"
