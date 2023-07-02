from bs4 import BeautifulSoup


class ParseInfo:
    async def search_ticer(self, response: str, ticer: str):
        soup = BeautifulSoup(response, 'lxml')

        try:
            qoutes = soup.find_all('a', class_='js-inner-all-results-quote-item')

            for qoute in qoutes:
                result_ticer = qoute.find('span', class_='second').text.strip().lower()
                result_equities = qoute.get('href').split('/')[-1].strip()
                result_exchange = qoute.find_all('span')[-1].text.split(' ')[-2].strip()

                if result_ticer == ticer:
                    return {
                        'ticker': result_ticer,
                        'equities': result_equities,
                        'exchange': result_exchange
                    }
            return False

        except:
            return False


    async def parse_investing_main(self, response: str, equity):
        soup = BeautifulSoup(response, 'lxml')

        try:
            name = soup.find('h1').text.strip()
            if name == '404':
                name = 'Данные отсутсвуют'
        except:
            name = '-'

        try:
            market_cap = soup.find('dd', attrs={'data-test':'marketCap'}).text.strip()
        except:
            market_cap = '-'

        try:
            dividend = soup.find('dd', attrs={'data-test':'dividend'}).text.strip()
        except:
            dividend = '-'

        try:
            p_e_ratio = soup.find('dd', attrs={'data-test':'ratio'}).text.strip()
        except:
            p_e_ratio = '-'

        try:
            shares_outstanding = soup.find('dd', attrs={'data-test':'sharesOutstanding'}).text.strip()
        except:
            shares_outstanding = '-'

        try:
            sector_parent = soup.find('a', attrs={'data-test':'link-company-profile'}).parent
            sector_parent = sector_parent.parent
            industry = sector_parent.find('div').find_all('a')[0].text.strip()
            sector = sector_parent.find('div').find_all('a')[1].text.strip()
        except:
            sector = '-'
            industry = '-'

        return {
            'name': name,
            'market_cap': market_cap,
            'dividend': dividend,
            'p_e_ratio': p_e_ratio,
            'shares_outstanding': shares_outstanding,
            'industry': industry,
            'sector': sector
        }


    async def parse_investing_balance_sheet(self, response: str, equity):
        soup = BeautifulSoup(response, 'lxml')

        try:
            interim = soup.find('a', attrs={'data-ptype':'Interim'}, class_='toggled').text.strip()
        except:
            interim = False

        try:
            annual = soup.find('a', attrs={'data-ptype':'Annual'}, class_='toggled').text.strip()
        except:
            annual = False

        try:
            tables_list = soup.find('table', class_='genTbl reportTbl').find_all('table', class_='genTbl reportTbl')

            total_current_assets = tables_list[0].find_all('tr')
            total_assets = tables_list[1].find_all('tr')
        except:
            total_current_assets = []
            total_assets = []

        cash_and_short_term_investments = await self.find_investing_financials(total_current_assets, 'Cash and Short Term Investments')
        long_term_investments = await self.find_investing_financials(total_assets, 'Long Term Investments')
        note_receivable_long_term = await self.find_investing_financials(total_assets, 'Note Receivable - Long Term')

        report = '-'

        if interim == 'Quarterly':
            report = 'Квартальный'

        if annual == 'Annual':
            report = 'Годовой'

        return {
            'cash_and_short_term_investments': cash_and_short_term_investments,
            'long_term_investments': long_term_investments,
            'note_receivable_long_term': note_receivable_long_term,
            'report': report
        }


    # Проверка по коэффициенту
    # async def parse_investing_ratios(response, equity):
    #     soup = BeautifulSoup(response, 'lxml')

    #     try:
    #         table_tr_list = soup.find('table', class_='genTbl reportTbl ratioTable').find('tbody').find_all('tr', {'id': 'childTr'})

    #         price_to_book_tr = table_tr_list[0].find('tbody').find_all('tr')
    #         total_debt_to_equity_tr = table_tr_list[5].find('tbody').find_all('tr')
    #     except:
    #         price_to_book_tr = []
    #         total_debt_to_equity_tr = []

    #     price_to_book = await find_investing_financials(price_to_book_tr, 'Price to Book MRQ')
    #     total_debt_to_equity = await find_investing_financials(total_debt_to_equity_tr, 'Total Debt to Equity MRQ')

    #     return {
    #         'price_to_book': price_to_book,
    #         'total_debt_to_equity': total_debt_to_equity
    #     }


    # Проверка по балансу
    async def parse_investing_balance_debt(self, response: str, equity):
        soup = BeautifulSoup(response, 'lxml')

        try:
            tables_list = soup.find('table', class_='genTbl reportTbl').find_all('table', class_='genTbl reportTbl')

            total_liabilities_tr = tables_list[3].find_all('tr')
            total_current_liabilities_tr = tables_list[2].find_all('tr')
        except:
            total_liabilities_tr = []
            total_current_liabilities_tr = []

        notes_payable_short_term_debt = await self.find_investing_financials(total_current_liabilities_tr, 'Notes Payable/Short Term Debt')
        other_current_liabilities_total = await self.find_investing_financials(total_current_liabilities_tr, 'Other Current liabilities, Total')
        long_term_debt = await self.find_investing_financials(total_liabilities_tr, 'Long Term Debt')

        return {
            'notes_payable_short_term_debt': notes_payable_short_term_debt,
            'other_current_liabilities_total': other_current_liabilities_total,
            'long_term_debt': long_term_debt
        }


    async def parse_marketwatch_financials(self, response: str, equty):
        soup = BeautifulSoup(response, 'lxml')

        try:
            table_body = soup.find('tbody', class_='table__body')
            tr_list = table_body.find_all('tr')
        except:
            tr_list = []

        sales_revenue = await self.find_marketwach_income_statsment(tr_list, 'Sales/Revenue')
        non_operating_interest_income = await self.find_marketwach_income_statsment(tr_list, 'Non-Operating Interest Income')

        return {
            'sales_revenue': sales_revenue,
            'non_operating_interest_income': non_operating_interest_income
        }


    async def find_investing_financials(self, tr_list: list, look_for: str):
        try:
            for item in tr_list:
                td_list = item.find_all('td')
                element_name = td_list[0].text.strip()

                if element_name == look_for:
                    return td_list[1].text.strip()
            return '-'
        except:
            return '-'


    async def find_marketwach_income_statsment(self, tr_list: list, look_for: str):
        try:
            for item in tr_list:
                td_list = item.find_all('td')

                income_statsment_title = td_list[0].find('div').text.strip()

                if income_statsment_title == look_for:
                    return td_list[-2].find('div').text.strip()
            return '-'
        except:
            return '-'