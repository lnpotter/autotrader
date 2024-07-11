import os
import datetime
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver import get_selenium_webdriver

# URLs e constantes
START_TIME = datetime.time(10, 0, 0)
END_TIME = datetime.time(16, 54, 0)
URL_CLEAR_LOGIN = "https://login.clear.com.br/pit/login/"
URL_CLEAR_TESOURO = "https://pro.clear.com.br/#renda-fixa/tesouro-direto"
URL_CLEAR = "https://pro.clear.com.br/#renda-variavel/swing-trade"

# Variáveis de ambiente (exemplo, substitua pelos seus valores reais)
CPF = os.getenv("CPF")
DATA_NASCIMENTO = os.getenv("DATA_NASCIMENTO")
SENHA = os.getenv("SENHA")
ASSINATURA = os.getenv("ASSINATURA")
SALDO_EXTERNO = float(os.getenv("SALDO_EXTERNO"))
STEP = int(os.getenv("STEP"))  # Passo inicial para otimização

# Parâmetros de trading
PRECO_HIGH_2A = 19
PRECO_LOW_2A = 12.81
DIFF_2A = PRECO_HIGH_2A - PRECO_LOW_2A

def time_in_range(start, end, current):
    """Verifica se o horário está dentro do intervalo especificado."""
    return start <= current <= end

def login_clear(driver):
    """Realiza o login na plataforma Clear."""
    driver.get(URL_CLEAR_LOGIN)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'Username'))).send_keys(CPF)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'DoB'))).send_keys(DATA_NASCIMENTO)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'Password'))).send_keys(SENHA)
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, 'bt_signin'))).click()
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CLASS_NAME, 'menu')))

def get_saldo_tesouro(driver):
    """Obtém o saldo do Tesouro Direto."""
    driver.get(URL_CLEAR_TESOURO)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "site")))
    driver.switch_to.frame(driver.find_element(By.NAME, "content-page"))
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[@class='btn-top-res btn-results btn-icon btn-text']")))
    sleep(2)
    saldo_tesouro = float(driver.find_element(By.XPATH, "//div[@class='text-value position-value-net']").text.replace("R$ ","").replace(".", "").replace(",","."))
    return saldo_tesouro

def trade_operations(driver, saldo_clear, saldo_tesouro, ticker, step):
    """Realiza as operações de compra e venda para um determinado ativo."""
    try:
        if saldo_clear >= saldo_tesouro:
            quantidade = int(driver.find_element(By.XPATH, "//div[@class='value detailed-net-qty']").text.split(" ")[0].replace(".", ""))
            preco_medio = float(driver.find_element(By.XPATH, "//div[@class='value detailed-net-average']").text.replace("R$ ","").replace(".", "").replace(",","."))
            preco_atual = float(driver.find_element(By.XPATH, "//span[@class='symbol-price']").text.replace(".","").replace(",","."))

            patrimonio = saldo_clear + SALDO_EXTERNO + quantidade * preco_atual
            diff_percentual = 1 - ((preco_atual - PRECO_LOW_2A) / DIFF_2A)
            quantidade_otimizada = ((patrimonio * diff_percentual) - (quantidade * preco_medio)) / preco_atual

            if quantidade_otimizada >= step:
                # Efetua compra
                driver.find_element(By.XPATH, f"//li[@class='action-item buy']/a[contains(text(), '{ticker}')]").click()
                driver.find_element(By.XPATH, "//input[@class='xbig input-quantity id-input-quantity ui-spinner-input']").send_keys(step)
                print(f"Efetuada a compra de {step} {ticker}")
                sleep(5)

            if quantidade_otimizada <= -step and preco_atual <= preco_medio:
                # Efetua venda
                driver.find_element(By.XPATH, f"//li[@class='action-item sell']/a[contains(text(), '{ticker}')]").click()
                driver.find_element(By.XPATH, "//input[@class='xbig input-quantity id-input-quantity ui-spinner-input']").send_keys(step)
                print(f"Efetuada a venda de {step} {ticker}")
                sleep(5)

    except Exception as e:
        print(f"Erro durante as operações de trading para {ticker}: {e}")

def main():
    driver = get_selenium_webdriver(headless=False)

    try:
        login_clear(driver)
        saldo_tesouro = get_saldo_tesouro(driver)

        while True:
            if not time_in_range(START_TIME, END_TIME, datetime.datetime.now().time()) or datetime.datetime.now().weekday() > 4:
                print(f"Pregão fechado. Horário: {datetime.datetime.now()}")
                continue

            driver.get(URL_CLEAR)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "site")))
            driver.switch_to.frame(driver.find_element(By.NAME, "content-page"))
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//div[@class='cont_detail detail-deal-book']")))

            saldo_clear = float(driver.find_element(By.XPATH, "//soma-paragraph[@class='total-amount total_val elipsed-val soma-paragraph hydrated small-text']").text.replace("R$ ","").replace(".", "").replace(",","."))
            saldo = saldo_clear + SALDO_EXTERNO
            print(f"Saldo projetado Clear: R${saldo_clear}")
            print(f"Saldo total dinheiro: R${saldo}")

            # Exemplo de uso para o ativo ABEV3
            trade_operations(driver, saldo_clear, saldo_tesouro, "ABEV3", STEP)

            driver.switch_to.default_content()
            sleep(2)

    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()