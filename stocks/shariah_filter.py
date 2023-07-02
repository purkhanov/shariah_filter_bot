import re
from stocks.stock_info import main_search


async def shariah_filter(ticer: str):
    ticer = ticer.lower()
    stock_info = await main_search(ticer)

    if not stock_info:
        return stock_info

    deposit_mc = await deposit_mc_func(stock_info['market_cap'],
                                       stock_info['cash_and_short_term_investments'],
                                       stock_info['long_term_investments'],
                                       stock_info['long_term_investments'])

    # # debt_mc = await debt_mc_func(parse_info['price_to_book'], parse_info['total_debt_to_equity'])
    debt_mc = await debt_mc_func_balance(
        stock_info['market_cap'],
        stock_info['notes_payable_short_term_debt'],
        stock_info['other_current_liabilities_total'],
        stock_info['long_term_debt'])

    fr_revenue = await fr_revenue_func(stock_info['sales_revenue'], stock_info['non_operating_interest_income'])
    forbidden_income = await share_of_forbidden_income(stock_info['shares_outstanding'], stock_info['non_operating_interest_income'])

    data = stock_info
    data['deposit_mc'] = deposit_mc
    data['debt_mc'] = debt_mc
    data['fr_revenue'] = fr_revenue
    data['forbidden_income'] = forbidden_income

    return data


async def deposit_mc_func(market_cap, cash_and_short_term_investments, long_term_investments, note_receivable_long_term):
    mc_in_million = await to_million(market_cap)
    cash_and_short_term_investments = await to_int(cash_and_short_term_investments)
    long_term_investments = await to_int(long_term_investments)
    note_receivable_long_term = await to_int(note_receivable_long_term)

    deposit = cash_and_short_term_investments + long_term_investments + note_receivable_long_term

    if deposit and mc_in_million:
        return str(round((deposit / mc_in_million) * 100, 1)) + '%'
    return '-'


# Проверка по коэффициенту
# async def debt_mc_func(price_to_book, total_debt_to_equity):
#     price_to_book = await to_int(price_to_book)
#     total_debt_to_equity = await to_int(total_debt_to_equity.replace('%', ''))

#     if price_to_book and total_debt_to_equity:
#         debt_mc = round(((total_debt_to_equity / 100) / price_to_book) * 100, 2)
#         return str(debt_mc) + '%'
#     return '-'


# Проверка по балансу
async def debt_mc_func_balance(m_cap: str,
                               notes_payable_short_term_debt: str,
                               total_debt_other_current_liabilities_totalto_equity: str,
                               long_term_debt: str) -> str:

    market_cap = await to_million(m_cap)
    notes_payable_short_term_debt = await to_int(notes_payable_short_term_debt)
    total_debt_other_current_liabilities_totalto_equity = await to_int(total_debt_other_current_liabilities_totalto_equity)
    long_term_debt = await to_int(long_term_debt)

    if notes_payable_short_term_debt and total_debt_other_current_liabilities_totalto_equity and long_term_debt:
        debt = notes_payable_short_term_debt + total_debt_other_current_liabilities_totalto_equity + long_term_debt
        debt_mc = round((debt / market_cap) * 100, 2)
        return str(debt_mc) + '%'
    return '-'


async def fr_revenue_func(sales_revenue: str, non_operating_interest_income: str) -> str:

    sr = await to_million(sales_revenue)
    n_oii = await to_million(non_operating_interest_income)

    if sr and n_oii:
        return str(round((n_oii / sr) * 100, 2)) + '%'
    return '-'


async def share_of_forbidden_income(shares_outstanding: str, n_oii: str) -> str:
    try:
        shares_outstanding = int(re.sub(r'\.|,', '', shares_outstanding))
    except:
        shares_outstanding = 0

    n_oii_in_million = await to_million(n_oii, to_real=True)

    if shares_outstanding and n_oii_in_million:
        return str(n_oii_in_million / shares_outstanding)
    return '-'


async def to_million(num_to_million: str, to_real: bool = False) -> int:
    if num_to_million == '-':
        return 0

    symbol = ''.join(re.findall(r'[A-Z]', num_to_million))
    number = re.sub(r'[A-Z]', '', num_to_million)
    splitted_num = re.split(r'\.|,', number)
    num_after_dot = splitted_num[-1]

    in_million = ''.join(splitted_num)
    match symbol:
        case 'M':
            if len(splitted_num) == 1:
                in_million += '0' * 6
            else:
                for i in range(1, 7):
                    if i == len(num_after_dot):
                        in_million += '0' * (6 - i)
                        break

        case 'B':
            if len(splitted_num) == 1:
                in_million += '0' * 9
            else:
                for i in range(1, 10):
                    if i == len(num_after_dot):
                        in_million += '0' * (9 - i)
                        break

        case 'T':
            if len(splitted_num) == 1:
                in_million += '0' * 12
            else:
                for i in range(1, 10):
                    if i == len(num_after_dot):
                        in_million += '0' * (12 - i)
                        break
    if to_real:
        return int(in_million)

    return int(in_million) / 1000000


async def to_int(string: str) -> float:
    if string == '-':
        return 0
    return float(string)