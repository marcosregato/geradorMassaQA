from faker import Faker
import random
import csv
from urllib.error import HTTPError
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

arquivoCSV = "./massaTeste.csv"

def geradorMassaFake(qtdMassa):

    faker = Faker('pt_BR')
    list =[]
    id = 1
    telefone = str(random.randint(1,9))+str(random.randint(0,9))+\
               str(random.randint(0,9))+str(random.randint(0,9))+\
               str(random.randint(0,9))+str(random.randint(0,9))+\
               str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
    try:
        for n in range(qtdMassa):
            dic = faker.profile()

            '''
            infoPessoa = [{'id':str(id),'nome': faker.name(), 'telefone': str(telefone), \
                          'endereco': faker.street_address(), 'barrio': faker.bairro(), \
                          'cidade': faker.city(), 'estado': faker.estado_nome(), \
                          'cep': faker.postcode(), 'email': faker.safe_email()
                        }]
            '''

            infoPessoa = [str(id),faker.name(),  str(telefone), \
                          faker.street_address(), faker.bairro(), \
                          faker.city(), faker.estado_nome(), \
                          faker.postcode(), faker.safe_email()
                           ]

            id =1+id
            list.append(infoPessoa)

        return list

    except IOError:
        print("I/O error")

'''
O browser ficara em background
'''
def geradorMassaSelenium(qtdMassa):
    try:
        url = "https://www.4devs.com.br/gerador_de_pessoas"
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

        list=[]
        id =1
        for qtd in range(qtdMassa):
            driver.get(url)
            time.sleep(5)

            driver.find_element_by_id("bt_gerar_pessoa").click()
            nome = driver.find_element_by_id("nome")
            telefone = driver.find_element_by_id("telefone_fixo")
            endereco = driver.find_element_by_id("endereco")
            bairro = driver.find_element_by_id("bairro")
            cidade = driver.find_element_by_id("cidade")
            estado = driver.find_element_by_id("estado")
            cep = driver.find_element_by_id("cep")
            email = driver.find_element_by_id("email")

            time.sleep(2)
            '''
            infoPessoa = [{'id':str(id),'nome': nome.text, 'telefone': telefone.text,\
                          'endereco': endereco.text,'barrio': bairro.text,\
                          'cidade': cidade.text,'estado': estado.text,\
                          'cep': cep.text,'email': email.text
                        }]
            '''
            infoPessoa = [str(id), nome.text, telefone.text, \
                           endereco.text, bairro.text, \
                           cidade.text, estado.text, \
                           cep.text, email.text
                           ]

            id = 1 + id
            list.append(infoPessoa)

        driver.quit()
        return list

    except HTTPError as e:
        print(e)

def gerarMassa(listInfo):
    try:
        print(listInfo)
        #col = ['nome','telefone','endereco','bairro','cidade','estado','cep','email']
        with open(arquivoCSV, 'w', newline='') as arqCSV:
            writer = csv.writer(arqCSV)
            writer.writerows(listInfo)

    except Exception as e:
        print(e)

gerarMassa(geradorMassaSelenium(10))