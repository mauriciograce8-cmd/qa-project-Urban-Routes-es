from selenium.webdriver.common.by import By


class UrbanRoutesPage:
    # Direcciones
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_btn = (By.XPATH, "//button[text()='Pedir un taxi']")

    # Tarifas
    comfort_tariff = (By.XPATH, "//*[contains(text(),'Comfort')]")
    # Este selector ayuda a verificar si la tarifa está seleccionada (basado en el diseño típico)
    comfort_card_active = (By.XPATH, "//div[contains(@class, 'tapps-card') and .//*[contains(text(),'Comfort')]]")

    # Teléfono
    phone_btn = (By.CLASS_NAME, 'np-button')
    phone_input = (By.ID, 'phone')
    next_btn = (By.XPATH, "//button[text()='Siguiente']")
    sms_input = (By.ID, 'code')
    confirm_sms_btn = (By.XPATH, "//button[text()='Confirmar']")

    # Tarjeta
    payment_method_btn = (By.CLASS_NAME, 'pp-button')
    add_card_btn = (By.XPATH, "//div[text()='Agregar tarjeta']")
    card_num_field = (By.ID, 'number')
    card_code_field = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    add_confirm_btn = (By.XPATH, "//button[text()='Agregar']")
    close_payment_modal = (By.XPATH, "//div[@class='payment-picker open']//button[@class='close-button section-close']")
    card_added_info = (By.CLASS_NAME, 'pp-value-text')  # Para verificar tarjeta

    # Extras
    comment_field = (By.ID, 'comment')
    blanket_switch = (By.XPATH, "//*[@class='switch']")
    blanket_input = (By.XPATH, "//*[@class='switch-input']")  # Para verificar estado
    ice_cream_plus = (By.XPATH, "//div[text()='Helado']/..//div[@class='counter-plus']")
    ice_cream_counter = (By.XPATH, "//div[text()='Helado']/..//div[@class='counter-value']")

    # Final
    order_btn = (By.CLASS_NAME, 'smart-button')
    order_header = (By.CLASS_NAME, 'order-header-content')

    def __init__(self, driver):
        self.driver = driver