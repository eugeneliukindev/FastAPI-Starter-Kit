import re


def camel_case_to_snake_case(input_str: str) -> str:
    """
    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo'
    >>> camel_case_to_snake_case("UserORM")
    'user'
    """
    if input_str.lower().endswith("orm"):
        input_str = input_str[:-3]

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", input_str)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)

    return s2.lower()
