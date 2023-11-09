import PySimpleGUI as sg
import fitz  # PyMuPDF
from googletrans import Translator

#classe 
class Tradutor():
    #tela do projeto com suas estilizaçoes
    def __init__(self):
        layout = [
            [sg.Text("Bem Vindo\n\n")],
            [sg.Text("Digite o caminho do pdf")],
            [sg.Input()],
            [sg.Button("Tradução", key='bt_t', size=(10, 1))]
        ]

        #atribuido a janela
        self.window = sg.Window("Tradução", layout=layout)

        #mantendo aberta enquanto os eventoes não sao acionados 
        while True:
            self.event, self.value = self.window.read()
            if self.event == sg.WIN_CLOSED:
                break
            elif self.event == "bt_t":
                self.leitura()

    #leitura do pdf 
    def leitura(self):
        try:
            caminho_pdf = self.value[0]
            documento_pdf = fitz.open(caminho_pdf)

        # Obtém o título do documento (nome do livro)
            #titulo_documento = documento_pdf.get_metadata("title")
            #print(f"Título do Livro: {titulo_documento}")

            total_paginas = documento_pdf.page_count
            print(f"Total de páginas: {total_paginas}")

            novo_pdf = fitz.open()

            for pagina_num in range(total_paginas):
                pagina = documento_pdf[pagina_num]
                text = pagina.get_text("text")

            # Verifica se o texto não é None antes de usar
                if text is not None:
                    print(f"Texto da página {pagina_num + 1}:\n{text}")

                    texto_traduzido = self.traduzir_texto(text, 'pt')

                # Verifica se o texto traduzido não é None antes de usar
                    if texto_traduzido is not None:
                        self.adicionar_pagina_pdf(novo_pdf, texto_traduzido)

            caminho_saida = "output_traduzido.pdf"
            novo_pdf.save(caminho_saida)
            novo_pdf.close()

            print(f"Novo PDF criado em: {caminho_saida}")

        except Exception as e:
            print(f"Erro: {e}")


    #função que fara a tradução de cada texto extradido 
    def traduzir_texto(self, texto, destino='pt'):
        translator = Translator()
        traducao = translator.translate(texto, dest=destino)
        print(f"Texto Traduzido:\n{traducao.text}")
        return traducao.text

    #função que criara o novo pdf com o texto traduzido 
    def adicionar_pagina_pdf(self, pdf_writer, texto):
        nova_pagina = pdf_writer.new_page(width=600, height=800)
        nova_pagina.insert_text((10, 10), texto)




if __name__ == "__main__":
    tradutor = Tradutor()
