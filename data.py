# Здесь хранятся все изменяемые тестовые данные

positive_data = {
    'name': 'John Pork',
    'email': 'johndoe@example.com',
    'radio': 'Business',  # 'Business' или 'Personal'
    'checkboxes': ['Cash', 'Card'],  # список нужных value для чекбоксов, есть Cash, Card, Cryptocurrency
    'dropdown': 'B Service',  # значение атрибута value опции
    'message': 'Hello, this is a valid test message. LOOOOOOOOOl'
}

negative_data = {
    'invalid_email': 'user@domaincom' # неправильное значение
}