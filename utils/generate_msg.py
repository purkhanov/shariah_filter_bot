from aiogram.types import Message

async def shariah_filter_message(data, msg):
    if not data:
        return f'<b>{msg.upper()}</b> не найдено!\nПроверьте правильность тикера и напишите на англиском'

    deposit_mc = data['deposit_mc']
    deposit_mc_warning = '\n<i>Deposit/MC должен быть не более 30% (КРИТИЧЕСКИ ВАЖНО!</i>'
    if deposit_mc == '-':
        deposit_mc_warning = ''

    debt_mc = data['debt_mc']
    debt_mc_warning = '\n<i>DEBT/MC должен быть не более 30% (КРИТИЧЕСКИ ВАЖНО!</i>'
    if debt_mc == '-':
        debt_mc_warning = ''

    fr_revenue = data['fr_revenue']
    fr_revenue_warning = '\n<i>FR/Revenue должен быть не более 5% (КРИТИЧЕСКИ ВАЖНО!</i>'
    if fr_revenue == '-':
        fr_revenue_warning = ''

    not_info = ''
    if deposit_mc == '-' or debt_mc == '-' or fr_revenue == '-':
        not_info = '\n\n<strong>Некоторые данные недоступно❗️\nнеобходима ручная проверка</strong>'

    message = \
        f"<b>{data['name']}</b>\n"+ \
        f"Тикер:  <strong>{data['ticker'].upper()}</strong>\n" + \
        f"Биржа:  <strong>{data['exchange']}</strong>\n" +\
        f"Рыночная капитализация:  <strong>{data['market_cap']}</strong>\n" + \
        f"Дивиденды:  <strong>{data['dividend']}</strong>\n" + \
        f"Сектор:  <strong>{data['sector']}</strong>\n" + \
        f"Deposit/MC:  <strong>{deposit_mc}</strong>{deposit_mc_warning}\n" + \
        f"Debt/MC:  <strong>{debt_mc}</strong>{debt_mc_warning}\n" + \
        f"FR/Revenue:  <strong>{fr_revenue}</strong>{fr_revenue_warning}\n" + \
        f"Доля запретного дохода:  <strong>{data['forbidden_income']}</strong>" + \
        f"{not_info}"

    return message


async def client_info_message(message: Message):
    return f'User: <b>{message.from_user.first_name}</b>\n\
    Username: <b>{message.from_user.username}</b>\n\
    Looking for: <b>{message.text}</b>'