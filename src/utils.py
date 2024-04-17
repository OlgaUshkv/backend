import json

from src.dto import Operation


def get_operations(filename) -> list[Operation]:  # pragma: nocover
    operations: list[Operation] = []
    with open(filename, encoding='utf-8') as f:
        for data in json.load(f):
            if data:
                operation = Operation.init_from_dict(data)
                operations.append(operation)

    return operations


def filter_operation_by_state(*operations: Operation, state: str) -> list[Operation]:
    filter_operations: list[Operation] = []
    for operation in operations:
        if operation.state == state:
            filter_operations.append(operation)
    return filter_operations


def sort_operation_by_date(*operations: Operation) -> list[Operation]:
    return sorted(operations, key=lambda operation: operation.operation_date, reverse=True)
