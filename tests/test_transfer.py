def test_negative_amount_transfer(driver, base_url):
    """Баг №1: отрицательная сумма должна отклоняться"""
    driver.get(base_url)
    # Клик по рублям
    rub_card = driver.find_element("xpath", "//div[contains(@class, 'g-card')][1]")
    rub_card.click()
    # Ввод номера карты
    card_input = driver.find_element("css selector", "input[placeholder='0000 0000 0000 0000']")
    card_input.send_keys("1111111111111111")
    # Ввод отрицательной суммы
    amount_input = driver.find_element("xpath", "//h3[text()='Сумма перевода:']/following-sibling::input")
    amount_input.clear()
    amount_input.send_keys("-500")
    # Кнопка "Перевести"
    transfer_btn = driver.find_element("xpath", "//button[contains(text(), 'Перевести')]")
    transfer_btn.click()
    # Проверяем, что alert не содержит "принят банком"
    alert = driver.switch_to.alert
    assert "принят банком" not in alert.text, \
        f"Дефект: перевод с отрицательной суммой выполнен. Alert: {alert.text}"
    alert.accept()

def test_invalid_card_number(driver, base_url):
    """Баг №2: невалидный номер карты должен быть отклонён"""
    driver.get(base_url)
    rub_card = driver.find_element("xpath", "//div[contains(@class, 'g-card')][1]")
    rub_card.click()
    card_input = driver.find_element("css selector", "input[placeholder='0000 0000 0000 0000']")
    card_input.send_keys("0000000000000000")
    amount_input = driver.find_element("xpath", "//h3[text()='Сумма перевода:']/following-sibling::input")
    amount_input.clear()
    amount_input.send_keys("100")
    transfer_btn = driver.find_element("xpath", "//button[contains(text(), 'Перевести')]")
    transfer_btn.click()
    alert = driver.switch_to.alert
    assert "неверный" in alert.text.lower() or "luhn" in alert.text.lower(), \
        f"Ожидалась ошибка валидации карты, получено: {alert.text}"
    alert.accept()