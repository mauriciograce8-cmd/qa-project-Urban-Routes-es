import data
from helpers import retrieve_phone_code
from pages import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        cls.driver.get(data.urban_routes_url)
        cls.page = UrbanRoutesPage(cls.driver)

    def test_01_set_route(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.page.from_field)).send_keys(data.address_from)
        self.driver.find_element(*self.page.to_field).send_keys(data.address_to)

        assert self.driver.find_element(*self.page.from_field).get_attribute('value') == data.address_from
        assert self.driver.find_element(*self.page.to_field).get_attribute('value') == data.address_to

    def test_02_select_comfort_tariff(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.page.request_taxi_btn)).click()
        wait.until(EC.element_to_be_clickable(self.page.comfort_tariff)).click()
        # Verificación visual (depende de la app, usualmente cambia el estilo)
        assert "Comfort" in self.driver.find_element(*self.page.comfort_tariff).text

    def test_03_enter_phone_number(self):
        self.driver.find_element(*self.page.phone_btn).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.page.phone_input)).send_keys(
            data.phone_number)
        self.driver.find_element(*self.page.next_btn).click()
        assert self.driver.find_element(*self.page.phone_input).get_attribute('value') == data.phone_number

    def test_04_confirm_sms_code(self):
        sms = retrieve_phone_code(self.driver)
        sms_field = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.page.sms_input))
        sms_field.send_keys(sms)
        self.driver.find_element(*self.page.confirm_sms_btn).click()
        # Si el botón de teléfono ahora muestra el número, el SMS fue exitoso
        assert data.phone_number in self.driver.find_element(*self.page.phone_btn).text

    def test_05_add_payment_card(self):
        self.driver.find_element(*self.page.payment_method_btn).click()
        self.driver.find_element(*self.page.add_card_btn).click()

        num_in = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.page.card_num_field))
        num_in.send_keys(data.card_number)

        code_in = self.driver.find_element(*self.page.card_code_field)
        code_in.send_keys(data.card_code)
        code_in.send_keys(Keys.TAB)

        self.driver.execute_script("arguments[0].click();", self.driver.find_element(*self.page.add_confirm_btn))
        self.driver.execute_script("arguments[0].click();", self.driver.find_element(*self.page.close_payment_modal))

        assert "Tarjeta" in self.driver.find_element(*self.page.payment_method_btn).text

    def test_06_add_driver_message(self):
        self.driver.find_element(*self.page.comment_field).send_keys(data.message_for_driver)
        assert self.driver.find_element(*self.page.comment_field).get_attribute('value') == data.message_for_driver

    def test_07_toggle_blanket(self):
        self.driver.find_element(*self.page.blanket_switch).click()
        # Verificamos si el input oculto está seleccionado
        assert self.driver.find_element(*self.page.blanket_input).is_selected()

    def test_08_add_ice_cream(self):
        plus = self.driver.find_element(*self.page.ice_cream_plus)
        plus.click()
        plus.click()
        assert self.driver.find_element(*self.page.ice_cream_counter).text == '2'

    def test_09_request_taxi(self):
        self.driver.find_element(*self.page.order_btn).click()
        wait = WebDriverWait(self.driver, 15)
        assert wait.until(EC.visibility_of_element_located(self.page.order_header)).is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()








