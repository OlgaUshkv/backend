from datetime import datetime

from src.dto import Operation, Payment


def test_init_payment_from_str():
    payment = Payment.init_from_str('Visa Classic 6831982476737658')
    assert payment.name == 'Visa Classic'
    assert payment.number == '6831982476737658'


def test_safe_payment_for_amount():
    payment = Payment(name='Счет', number='75106830613657916952')
    assert payment.safe() == 'Счет **6952'


def test_safe_payment_for_card_number():
    payment = Payment(name='Maestro', number='1596837868705199')
    assert payment.safe() == 'Maestro 1596 83** **** 5199'


def test_split_card_number_by_blocks():
    card_number = '1596837868705199'
    result = Payment.split_card_number_by_blocks(card_number)
    assert result == '1596 8378 6870 5199'


def test_init_operation_from_dict(operation_data_without_from):
    operation = Operation.init_from_dict(operation_data_without_from)

    assert operation.id == 716496732
    assert operation.state == 'EXECUTED'
    assert operation.operation_date == datetime(2018, 4, 4, 17, 33, 34, 701093)
    assert operation.amount.value == 40701.91
    assert operation.amount.currency_name == 'USD'
    assert operation.amount.currency_code == 'USD'
    assert operation.description == 'Открытие вклада'
    assert operation.payment_to.name == 'Счет'
    assert operation.payment_to.number == '72731966109147704472'
    assert operation.payment_from is None


def test_operation_with_from(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    expected_result = (
        '04.04.2018 Перевод организации\n'
        'Visa Gold 5999 41** **** 6353 -> Счет **4472\n'
        '40701.91 USD'
    )

    assert operation.safe() == expected_result


def test_operation_without_from(operation_data_without_from):
    operation = Operation.init_from_dict(operation_data_without_from)
    expected_result = (
        '04.04.2018 Открытие вклада\n'
        'Счет **4472\n'
        '40701.91 USD'
    )

    assert operation.safe() == expected_result