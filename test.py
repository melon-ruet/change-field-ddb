from decimal import Decimal

import boto3
import moto

from models import ResultModel

with moto.mock_dynamodb2():
    region = 'eu-west-1'
    ResultModel.Meta.region = region
    ResultModel.create_table(wait=True)

    # Data
    result_map = {
        'semester 1': 3.75,
        'semester 2': 3.17,
        'semester 3': 3.90,
        'semester 4': 3.67
    }
    result_list = [3.75, 3.17, 3.90, 3.67]

    # Insert as Map with PynamoDB
    result1 = ResultModel(result=result_map)
    result1.save()
    assert ResultModel.count() == 1
    result1_id = result1.id
    print(result1_id)

    # Retrieve the data from inserted as list
    result1_retr = ResultModel.get(result1_id)
    assert result1_retr.result.attribute_values == result_map

    # Insert as list so it will convert and saved as map
    result2 = ResultModel(result=result_list)
    result2.save()
    assert ResultModel.count() == 2
    result2_id = result2.id
    print(result2_id)

    # Retrieve the data from inserted as list
    result2_retr = ResultModel.get(result2_id)
    assert result2_retr.result.attribute_values == result_map

    # Insert list value in result with boto3
    dynamodb = boto3.resource('dynamodb', region)
    table = dynamodb.Table(ResultModel.Meta.table_name)

    # float is not supported by boto3. But decimal is supported. So converted to Decimal
    item = [Decimal(str(v)) for v in result_list]
    # Updating item instead of creating because result is MapAttribute by default
    table.update_item(
        Key={'id': str(result1_id)},
        AttributeUpdates={
            'result': {'Value': item, 'Action': 'PUT'}
        }
    )

    assert table.get_item(Key={'id': str(result1_id)})['Item']['result'] == item

    # Retrieve the data that is a list in dynamodb
    result1_retr = ResultModel.get(result1_id)
    assert result1_retr.result.attribute_values == result_map
