# Standard Library
from inflection import camelize

# Documentation Library
from drf_yasg.inspectors import SwaggerAutoSchema


class CamelCaseOperationIDAutoSchema(SwaggerAutoSchema):
    """
    Convert to camel-case swagger displayed operations
    """

    def get_operation_id(self, operation_keys=None):
        operation_id = super().get_operation_id(operation_keys)
        return camelize(operation_id, uppercase_first_letter=False)
