from bs4 import BeautifulSoup
import re

html_text = '''
<div class="ui-tabs__content"><div><!----></div><div><!----></div><div><ol data-v-704f838a="" class="loan-requirements mb-24"><li>Копия всех страниц (включая пустые) паспорта Заемщика/Созаемщиков/Поручителя.</li><li>Копия СНИЛС Заемщика/Созаемщиков/Поручителя. При идентификации клиента через портал «Госуслуги»
        с&nbsp;получением Банком необходимых сведений о&nbsp;СНИЛС данный документ не&nbsp;является обязательным;</li><li>Копия свидетельства ИНН Заемщика/Созаемщиков/Поручителя. При идентификации клиента портал
        «Госуслуги» с&nbsp;получением Банком необходимых сведений об&nbsp;ИНН данный
        документ не&nbsp;является обязательным;</li><li>Документы, подтверждающие доход и&nbsp;трудоустройство заемщика/созаемщика/поручителя</li></ol> <div data-v-333339b4="" data-v-704f838a="" class="load-docs"><ul data-v-333339b4="" class="load-docs-list"></ul> <p data-v-333339b4="" class="load-docs__text"></p> <ul data-v-333339b4="" class="load-docs-additions"><li data-v-333339b4=""><h4 data-v-333339b4="" class="h4"></h4> <p data-v-333339b4="" class="load-docs__text"></p> <a data-v-333339b4="" href="/files/services/fiz/pdf/paket_documentov.pdf" target="_blank" rel="noopener noreferrer" class="load-docs__text load-docs__link flex items-center"><span data-v-333339b4=""></span> <p data-v-333339b4="">Пакет документов</p></a></li><li data-v-333339b4=""><h4 data-v-333339b4="" class="h4">
                Документы можно отправить в Банк без посещения офиса
                <a class="step-link" target="_blank" href="https://cib.app/uploaddocs">
                    по ссылке
                </a>
            </h4> <p data-v-333339b4="" class="load-docs__text"></p> <!----></li><li data-v-333339b4=""><h4 data-v-333339b4="" class="h4"></h4> <p data-v-333339b4="" class="load-docs__text">
                В&nbsp;случае если заемщик/созаемщики (поручитель) зарегистрирован в&nbsp;качестве
                индивидуального предпринимателя предоставляются также следующие документы:
            </p> <a data-v-333339b4="" href="/files/services/fiz/pdf/paket_documentov_ip.pdf" target="_blank" rel="noopener noreferrer" class="load-docs__text load-docs__link flex items-center"><span data-v-333339b4=""></span> <p data-v-333339b4="">Пакет документов для индивидуальных предпринимателей</p></a></li><li data-v-333339b4=""><h4 data-v-333339b4="" class="h4"></h4> <p data-v-333339b4="" class="load-docs__text">
                В&nbsp;случае если заемщик/созаемщики (поручитель) является налогоплательщиком налога
                на&nbsp;профессиональный доход (самозанятым):
            </p> <a data-v-333339b4="" href="/files/services/fiz/pdf/paket_documentov_samozanyatye.pdf" target="_blank" rel="noopener noreferrer" class="load-docs__text load-docs__link flex items-center"><span data-v-333339b4=""></span> <p data-v-333339b4="">Пакет документов для самозанятых</p></a></li><li data-v-333339b4=""><h4 data-v-333339b4="" class="h4">
                Документы можно отправить в Банк без посещения офиса
                <a class="step-link" target="_blank" href="https://cib.app/uploaddocs">
                    по ссылке
                </a>
            </h4> <p data-v-333339b4="" class="load-docs__text"></p> <!----></li><li data-v-333339b4=""><h4 data-v-333339b4="" class="h4"></h4> <p data-v-333339b4="" class="load-docs__text">
                В&nbsp;случае если заемщик/созаемщики (поручитель) являются собственниками бизнеса:
            </p> <a data-v-333339b4="" href="/files/services/fiz/pdf/paket_documentov_ul.pdf" target="_blank" rel="noopener noreferrer" class="load-docs__text load-docs__link flex items-center"><span data-v-333339b4=""></span> <p data-v-333339b4="">Пакет документов для собственников бизнеса</p></a></li><li data-v-333339b4=""><h4 data-v-333339b4="" class="h4"></h4> <p data-v-333339b4="" class="load-docs__text">
                В&nbsp;случае оформления поручительства&nbsp;— юридического лица, либо оформлении
                в&nbsp;залог по&nbsp;кредиту имущества, принадлежащего юридическому лицу:
            </p> <a data-v-333339b4="" href="/files/services/fiz/pdf/paket_documentov_ul_porychitel.pdf" target="_blank" rel="noopener noreferrer" class="load-docs__text load-docs__link flex items-center"><span data-v-333339b4=""></span> <p data-v-333339b4="">Пакет документов для поручителя юридического лица</p></a></li></ul> <p data-v-333339b4="" class="load-docs__text"><div class="mt-24 mb-16 fz-14 text-grey">
            Перечень документов не&nbsp;является исчерпывающим и&nbsp;может быть изменен с
            &nbsp;учетом предоставленных документов.
        </div></p> <ul data-v-333339b4="" class="load-docs-additions mt-32"><li data-v-333339b4=""><a data-v-333339b4="" href="/files/services/fiz/pdf/instructions-employment.pdf" target="_blank" rel="noopener noreferrer" class="load-docs__text load-docs__link flex items-center"><span data-v-333339b4=""></span> <p data-v-333339b4="">Инструкция по заказу  Сведений о трудовой деятельности</p></a></li><li data-v-333339b4=""><a data-v-333339b4="" href="/files/services/fiz/pdf/instructions-individual-personal-account.pdf" target="_blank" rel="noopener noreferrer" class="load-docs__text load-docs__link flex items-center"><span data-v-333339b4=""></span> <p data-v-333339b4="">Инструкция по заказу  Сведений о состоянии индивидуального лицевого счета застрахованного лица</p></a></li><li data-v-333339b4=""><a data-v-333339b4="" href="/files/services/fiz/pdf/instructions-income-individual.pdf" target="_blank" rel="noopener noreferrer" class="load-docs__text load-docs__link flex items-center"><span data-v-333339b4=""></span> <p data-v-333339b4="">Инструкция по заказу Сведений о доходах физического лица</p></a></li></ul></div></div><div><!----></div></div>
'''

soup = BeautifulSoup(html_text, 'html.parser')

# Извлечение заголовка
header = soup.find('div', class_='ui-tabs__content').find('div').text.strip()
print("Заголовок:", header)

# Извлечение текста без ссылки на PDF
text_without_link = soup.find_all('div', class_='ui-tabs__content')[1].text.strip()
print("Текст без ссылки на PDF:", text_without_link)

# Извлечение текста с ссылкой на PDF
text_with_link = soup.find_all('div', class_='ui-tabs__content')[2].text.strip()
pdf_link = soup.find_all('a', class_='load-docs__link')[0]['href']  # Первая ссылка на PDF
print("Текст с ссылкой на PDF:", text_with_link)
print("Ссылка на PDF:", pdf_link)
