import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_negative_amount_transfer(driver, base_url):
    """Баг №1: отрицательная сумма должна отклоняться"""
    driver.get(base_url)
    # Клик по рублям
    rub_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'g-card')][1]"))
    )
    rub_card.click()
    
    # Ввод номера карты
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']"))
    )
    card_input.send_keys("1111111111111111")
    
    # Ввод отрицательной суммы
    amount_input = driver.find_element(By.XPATH, "//h3[text()='Сумма перевода:']/following-sibling::input")
    amount_input.clear()
    amount_input.send_keys("-500")
    
    # Ожидаем появления кнопки "Перевести"
    transfer_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Перевести']"))
    )
    transfer_btn.click()
    
    # Проверяем alert
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert "принят банком" not in alert.text, \
        f"Дефект: перевод с отрицательной суммой выполнен. Alert: {alert.text}"
    alert.accept()


def test_invalid_card_number(driver, base_url):
    """Баг №2: невалидный номер карты должен быть отклонён"""
    driver.get(base_url)
    rub_card = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'g-card')][1]"))
    )
    rub_card.click()
    
    card_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']"))
    )
    card_input.send_keys("0000000000000000")
    
    amount_input = driver.find_element(By.XPATH, "//h3[text()='Сумма перевода:']/following-sibling::input")
    amount_input.clear()
    amount_input.send_keys("100")
    
    transfer_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Перевести']"))
    )
    transfer_btn.click()
    
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert "неверный" in alert.text.lower() or "luhn" in alert.text.lower(), \
        f"Ожидалась ошибка валидации карты, получено: {alert.text}"
    alert.accept()