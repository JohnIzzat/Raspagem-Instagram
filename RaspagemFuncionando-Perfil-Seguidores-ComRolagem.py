import selenium
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Configuração do Selenium WebDriver
option = Options()
option.add_argument('--start-maximized')
driver = webdriver.Chrome(options=option)
print('[AVISO] Aguarde 10 segundos que será informado seu login e senha automaticamente.')
driver.get('https://instagram.com')
sleep(10)

# Tentativa de Login
while True:
    try:
        login = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        login.send_keys("#")  # Substitua por seu login
        senha = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        senha.send_keys("#")  # Substitua por sua senha
        entrar = driver.find_element(By.XPATH, '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1xmf6yo x1e56ztr x540dpk x1m39q7l x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
        entrar.click()
        print("Login efetuado")
        break
    except Exception as e:
        print(f"Erro ao tentar logar: {e}")

# Aguardar a página carregar
sleep(15)

# Navegar até o perfil do usuário
driver.get('https://www.instagram.com/')
sleep(6)

# Clicar em seguidores
while True:
    try:
        seguidores = driver.find_element(By.XPATH, "//a[contains(@href, 'followers')]")
        seguidores.click()
        print("Consegui clicar em seguidores!")
        break
    except Exception as e:
        print(f"Erro ao tentar clicar em seguidores: {e}")

# Esperar o modal carregar
sleep(8)

# Lista para armazenar os nomes dos seguidores
dados_usuarios = []

# Realizar a rolagem e raspagem dos seguidores
try:
    # Esperar o modal de seguidores aparecer
    modal_seguidores = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']"))
    )
    last_height = driver.execute_script("return arguments[0].scrollHeight;", modal_seguidores)

    while True:
        # Coletar os nomes visíveis no modal de seguidores
        nomes = driver.find_elements(By.XPATH, "//span[@class='_ap3a _aaco _aacw _aacx _aad7 _aade']")
        for nome in nomes:
            texto_nome = nome.text.strip()
            if texto_nome and texto_nome not in dados_usuarios:  # Verificar se o nome não está vazio e evitar duplicados
                dados_usuarios.append(texto_nome)
                print(texto_nome)

        # Rolar a lista de seguidores para baixo
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", modal_seguidores)
        sleep(2)  # Tempo para carregar o novo conteúdo

        # Verificar se chegamos ao final da rolagem
        new_height = driver.execute_script("return arguments[0].scrollHeight;", modal_seguidores)
        if new_height == last_height:
            print("Fim da lista de seguidores.")
            break
        last_height = new_height

except Exception as e:
    print(f"Erro durante a raspagem ou rolagem: {e}")

# Salvando dados em um arquivo txt
nome_arquivo = "usuarios.txt"
with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
    for nome in dados_usuarios:
        arquivo.write(nome + '\n')

print(f"Dados salvos no arquivo {nome_arquivo}.")
input('')