from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# Функции помощники
def scroll_and_wait_clickable(driver, wait, locator, timeout=10, block='center'):
    """
    Скроллит до элемента, дожидается, что он станет кликабельным, и возвращает его.
    :param driver: WebDriver
    :param wait: WebDriverWait instance
    :param locator: кортеж (By, locator_string)
    :param timeout: время ожидания
    :param block: положение блока при скролле: 'start', 'center', 'end', 'nearest'
    """
    # Дождаться присутствия элемента в DOM
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
    # Прокрутить до элемента
    driver.execute_script("arguments[0].scrollIntoView({block: '%s'});" % block, element)
    # Дождаться, что элемент станет кликабельным
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))