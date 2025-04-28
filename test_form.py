# Климанов Григорий
# Позитивный и негативный автотесты

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pytest

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


from data import positive_data
from data import negative_data
from helper import scroll_and_wait_clickable


BASE_URL = "https://qatest.datasub.com/"

NAME_INPUT_FIELD_XPATH = "//form[@id='subscriptionForm']/div/div/input[@id='name']"
EMAIL_INPUT_FIELD_XPATH = "//form[@id='subscriptionForm']/div/div/input[@id='email']"
SUBMIT_BUTTON_XPATH = "//form[@id='subscriptionForm']/div/div/button"

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    browser = request.param
    
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
    
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(options=options)
    
    else:
        raise Exception(f"Unsupported browser: {browser}")

    driver.get(BASE_URL)

    yield driver
    driver.quit()


# Позитивная проверка -- форму можно отправить при всех введенных полях, заполненными валидными данными
# DoP (Definition Of Passed) - появилась надпись, о том, что форма отправлена

def test_form_successfully_submits_with_valid_data(driver, expected_success_text='Форма отправлена.'):
    wait = WebDriverWait(driver, 10)

    # 1. Имя
    name_input = scroll_and_wait_clickable(
        driver, wait, (By.XPATH, NAME_INPUT_FIELD_XPATH)
    )
    name_input.clear()
    name_input.send_keys(positive_data['name'])

    # 2. Email
    email_input = scroll_and_wait_clickable(
        driver, wait, (By.XPATH, EMAIL_INPUT_FIELD_XPATH)
    )
    email_input.clear()
    email_input.send_keys(positive_data['email'])

    # 3. Radio
    radio_locator = (By.XPATH, f"//input[@value='{positive_data['radio']}']")
    business_radio = scroll_and_wait_clickable(driver, wait, radio_locator)
    business_radio.click()

    # 4. Checkbox(es)
    for val in positive_data['checkboxes']:
        cb_locator = (By.XPATH, f"//input[@value='{val}']")
        checkbox = scroll_and_wait_clickable(driver, wait, cb_locator)
        if not checkbox.is_selected():
            checkbox.click()

    # 5. Dropdown
    dropdown = scroll_and_wait_clickable(driver, wait, (By.TAG_NAME, "select"))
    dropdown.click()
    option = scroll_and_wait_clickable(
        driver, wait, (By.XPATH, f"//option[@value='{positive_data['dropdown']}']")
    )
    option.click()

    # 6. Textarea
    area = scroll_and_wait_clickable(driver, wait, (By.TAG_NAME, "textarea"))
    area.clear()
    area.send_keys(positive_data['message'])

    # 7. Submit
    submit = scroll_and_wait_clickable(driver, wait, (By.XPATH, SUBMIT_BUTTON_XPATH))
    submit.click()


    # Проверить, что надпись о успешной отправке высветилась
    success_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='formStatus']"))
    )
    assert expected_success_text == success_msg.text


# Негативная проверка -- форма не отправляется при всех заполненых полях, кроме поля email
# DoP (Definition Of Passed) - высветилась ошибка, т.е поле стало красным (из-за класса "is-invalid")

def test_form_shows_error_for_invalid_email(driver):
    wait = WebDriverWait(driver, 10)

    # 1. Заполняем все поля валидно, кроме email
    # Имя
    name_input = scroll_and_wait_clickable(driver, wait, (By.XPATH, NAME_INPUT_FIELD_XPATH))
    name_input.clear()
    name_input.send_keys(positive_data['name'])

    # Email — некорректный
    email_input = scroll_and_wait_clickable(driver, wait, (By.XPATH, EMAIL_INPUT_FIELD_XPATH))
    email_input.clear()
    email_input.send_keys(negative_data['invalid_email'])

    # Radio
    radio = scroll_and_wait_clickable(
        driver, wait, (By.XPATH, f"//input[@value='{positive_data['radio']}']")
    )
    radio.click()

    # Checkbox(es)
    for val in positive_data['checkboxes']:
        cb = scroll_and_wait_clickable(driver, wait, (By.XPATH, f"//input[@value='{val}']"))
        if not cb.is_selected():
            cb.click()

    # Dropdown
    dropdown = scroll_and_wait_clickable(driver, wait, (By.TAG_NAME, "select"))
    dropdown.click()
    option = scroll_and_wait_clickable(
        driver, wait, (By.XPATH, f"//option[@value='{positive_data['dropdown']}']")
    )
    option.click()

    # Textarea
    area = scroll_and_wait_clickable(driver, wait, (By.TAG_NAME, "textarea"))
    area.clear()
    area.send_keys(positive_data['message'])

    # Submit
    submit = scroll_and_wait_clickable(driver, wait, (By.XPATH, SUBMIT_BUTTON_XPATH))
    submit.click()

    # Проверяем, что к input у email добавился новый класс "is-invalid"
    email_input_after_submit = wait.until(
        EC.presence_of_element_located((By.XPATH, EMAIL_INPUT_FIELD_XPATH))
    )

    email_classes = email_input_after_submit.get_attribute("class")
    assert "is-invalid" in email_classes, f"Ожидается 'is-invalid' в классах, но там: {email_classes}"