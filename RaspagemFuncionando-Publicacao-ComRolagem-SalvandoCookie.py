import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pickle

# Configuração do Selenium WebDriver
def configurar_driver():
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    return driver

# Salvamento e carregamento de cookies
def salvar_cookies(driver, arquivo_cookie):
    with open(arquivo_cookie, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def carregar_cookies(driver, arquivo_cookie):
    if os.path.exists(arquivo_cookie):
        with open(arquivo_cookie, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        return True
    return False

# Login no Instagram
def realizar_login(driver, usuario, senha, arquivo_cookie):
    driver.get('https://instagram.com')
    sleep(5)

    if carregar_cookies(driver, arquivo_cookie):
        driver.refresh()
        sleep(5)
        print("[INFO] Cookies carregados, login automático realizado.")
        return True

    try:
        print("[INFO] Realizando login manual...")
        login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input'))
        )
        login.send_keys(usuario)

        senha_input = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        senha_input.send_keys(senha)

        entrar = driver.find_element(By.XPATH, '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1e56ztr x540dpk x1m39q7l x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
        entrar.click()

        WebDriverWait(driver, 15).until(EC.url_contains('instagram.com'))
        salvar_cookies(driver, arquivo_cookie)
        print("[INFO] Login realizado e cookies salvos.")
        return True
    except Exception as e:
        print(f"[ERRO] Falha no login: {e}")
        return False

# Raspagem de seguidores
def raspar_seguidores(driver, limite_usuarios):
    dados_usuarios = []

    try:
        # Acessando a publicação
        driver.get('https://www.instagram.com/p/DBbkwEbR9vA/')
        sleep(5)

        print("[INFO] Acessando lista de seguidores...")
        modal_seguidores = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='x5yr21d xw2csxc x1odjw0f x1n2onr6']"))
        )

        last_height = driver.execute_script("return arguments[0].scrollHeight;", modal_seguidores)

        while len(dados_usuarios) < limite_usuarios:
            nomes = driver.find_elements(By.XPATH, "//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade']")
            for nome in nomes:
                texto_nome = nome.text.strip()
                if texto_nome and texto_nome not in dados_usuarios:
                    dados_usuarios.append(texto_nome)
                    print(f"[INFO] Coletado: {texto_nome}")
                    if len(dados_usuarios) >= limite_usuarios:
                        break

            driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", modal_seguidores)
            sleep(5)

            new_height = driver.execute_script("return arguments[0].scrollHeight;", modal_seguidores)
            if new_height == last_height:
                break
            last_height = new_height

    except Exception as e:
        print(f"[ERRO] Falha durante a raspagem: {e}")

    return dados_usuarios

# Salvar os dados em arquivo
def salvar_dados(dados, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        for dado in dados:
            arquivo.write(dado + '\n')
    print(f"[INFO] Dados salvos no arquivo {nome_arquivo}.")

# Função principal
def main():
    usuario = ""  # Substitua pelo seu login
    senha = ""  # Substitua pela sua senha
    arquivo_cookie = "cookies.pkl"
    nome_arquivo = "usuarios.txt"

    limite_usuarios = int(input("Quantos seguidores deseja raspar? "))

    driver = configurar_driver()

    try:
        if not realizar_login(driver, usuario, senha, arquivo_cookie):
            print("[ERRO] Não foi possível realizar o login.")
            return

        dados_usuarios = raspar_seguidores(driver, limite_usuarios)
        salvar_dados(dados_usuarios, nome_arquivo)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()