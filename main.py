import data
import json
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def retrieve_phone_code(driver) -> str:
    code = None
    for i in range(15):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except Exception:
            time.sleep(1)
            continue
        if code: return code
    return "0000"


class UrbanRoutesPage:
    # Selectores Base
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_btn = (By.XPATH, "//button[text()='Pedir un taxi']")
    comfort_tariff = (By.XPATH, "//*[contains(text(),'Comfort')]")


    phone_btn = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    next_btn = (By.XPATH, "//button[text()='Siguiente']")
    sms_input = (By.ID, 'code')  # Este es el del SMS
    confirm_sms_btn = (By.XPATH, "//button[text()='Confirmar']")

    # Selectores Tarjeta
    payment_method_btn = (By.CLASS_NAME, 'pp-button')
    add_card_btn = (By.XPATH, "//div[text()='Agregar tarjeta']")
    card_num_field = (By.ID, 'number')
    # Usamos el contenedor padre para no confundirlo con el del SMS
    card_code_field = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    add_confirm_btn = (By.XPATH, "//button[text()='Agregar']")
    close_payment_modal = (By.XPATH, "//div[@class='payment-picker open']//button[@class='close-button section-close']")

    # Extras
    comment_field = (By.ID, 'comment')
    blanket_switch = (By.XPATH, "//*[@class='switch']")
    ice_cream_plus = (By.XPATH, "//div[text()='Helado']/..//div[@class='counter-plus']")
    order_btn = (By.CLASS_NAME, 'smart-button')
    order_header = (By.CLASS_NAME, 'order-header-content')

    def __init__(self, driver):
        self.driver = driver


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test_full_taxi_order(self):
        self.driver.get(data.urban_routes_url)
        page = UrbanRoutesPage(self.driver)
        wait = WebDriverWait(self.driver, 25)

        # 1. Direcciones
        wait.until(EC.visibility_of_element_located(page.from_field)).send_keys(data.address_from)
        self.driver.find_element(*page.to_field).send_keys(data.address_to)

        # 2. Comfort
        wait.until(EC.element_to_be_clickable(page.request_taxi_btn)).click()
        wait.until(EC.element_to_be_clickable(page.comfort_tariff)).click()

        # 3. Teléfono (Aquí se usa el código 5926 interceptado)
        self.driver.find_element(*page.phone_btn).click()
        wait.until(EC.visibility_of_element_located(page.phone_input)).send_keys(data.phone_number)
        self.driver.find_element(*page.next_btn).click()

        sms = retrieve_phone_code(self.driver)
        wait.until(EC.visibility_of_element_located(page.sms_input)).send_keys(sms)
        self.driver.find_element(*page.confirm_sms_btn).click()

        # 4. Tarjeta
        wait.until(EC.element_to_be_clickable(page.payment_method_btn)).click()
        wait.until(EC.element_to_be_clickable(page.add_card_btn)).click()

        num_in = wait.until(EC.visibility_of_element_located(page.card_num_field))
        num_in.send_keys(data.card_number)

        # IMPORTANTE:
        code_in = self.driver.find_element(*page.card_code_field)
        code_in.send_keys(data.card_code)
        code_in.send_keys(Keys.TAB)

        # Clic
        btn_add = self.driver.find_element(*page.add_confirm_btn)
        self.driver.execute_script("arguments[0].click();", btn_add)

        # Cerrar el modal
        btn_close = wait.until(EC.presence_of_element_located(page.close_payment_modal))
        self.driver.execute_script("arguments[0].click();", btn_close)

        # 5. Extras
        self.driver.find_element(*page.comment_field).send_keys(data.message_for_driver)
        self.driver.find_element(*page.blanket_switch).click()
        plus = self.driver.find_element(*page.ice_cream_plus)
        plus.click()
        plus.click()

        # 6. Pedir Taxi
        self.driver.find_element(*page.order_btn).click()

        # 7. Verificación
        assert wait.until(EC.visibility_of_element_located(page.order_header)).is_displayed()
        print("¡TODO FUNCIONÓ!")

    @classmethod
    def teardown_class(cls):
        time.sleep(5)
        cls.driver.quit()


if __name__ == "__main__":
    TestUrbanRoutes.setup_class()
    test = TestUrbanRoutes()
    try:
        test.test_full_taxi_order()
    finally:
        TestUrbanRoutes.teardown_class()
