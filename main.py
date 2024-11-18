from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

app = Flask(__name__)


@app.route("/search_videos", methods=["POST"])
def search_videos():
    # Obtém o termo de pesquisa enviado no corpo da requisição
    search_term = request.json.get("search_term", "")
    if not search_term:
        return jsonify({"error": "O campo 'search_term' é obrigatório"}), 400

    # Configuração do Selenium
    # Configuração do Chrome para execução
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    # Inicializa o WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(20)
    wait = WebDriverWait(driver, 20)

    try:
        # Navega até o site
        search_url = "https://randomyoutube.net/"
        driver.get(search_url)

        # Espera o site carregar e interage com o campo de pesquisa
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "swiper-slide")))
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    ".fa-duotone.fa-magnifying-glass.absolute.left-3.cursor-pointer.lg\\:pointer-events-none",
                )
            )
        ).click()

        form = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".relative.flex.items-center.px-0.w-full.h-40")
            )
        )
        search_input = form.find_element(By.TAG_NAME, "input")
        search_input.send_keys(search_term + Keys.ENTER)

        # Espera os resultados carregarem
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".text-sm.line-clamp-2"))
        )

        list_videos = driver.find_elements(
            By.CSS_SELECTOR,
            ".yt-video.lg\\:w-1\\/4.w-full.flex.flex-col.text-left.gap-3.cursor-pointer.bg-transparent",
        )

        # Cria o JSON com os resultados
        json_videos = []
        for i, video in enumerate(list_videos):
            json_videos.append({
                "Link_ID": video.get_attribute("href").split("=")[1],
                "Image": video.find_element(By.TAG_NAME, "img").get_attribute("src"),
                "Title": video.find_element(By.TAG_NAME, "vid-title-string").text,
            })

        return jsonify(json_videos)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        driver.quit()


if __name__ == "__main__":
    app.run(debug=True)
