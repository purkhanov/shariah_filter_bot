import asyncio, aiohttp
from aiohttp import ClientSession
from stocks.parse_info import ParseInfo
from config import headers


async def get_parse_info(session: ClientSession, parser_func: ParseInfo, url: str, ticer: str):
    async with session.get(url) as request:
        response = await request.text()
        return await parser_func(response, ticer)


async def get_all(session: ClientSession, parser: ParseInfo, search_result: dict, ticer: str):
    func_list = [
        {
            'url': f'https://www.investing.com/equities/{search_result["equities"]}',
            'function': parser.parse_investing_main
        },
        {
            'url': f'https://www.investing.com/equities/{search_result["equities"]}-balance-sheet',
            'function': parser.parse_investing_balance_sheet
        },
        {
            'url': f'https://www.investing.com/equities/{search_result["equities"]}-balance-sheet',
            'function': parser.parse_investing_balance_debt
        },
        {
            'url': f'https://www.marketwatch.com/investing/stock/{search_result["ticker"]}/financials?mod=mw_quote_tab',
            'function': parser.parse_marketwatch_financials
        }
    ]

    tasks = []
    for func in func_list:
        task = asyncio.create_task(get_parse_info(session, func['function'], func['url'], ticer))
        tasks.append(task)

    data = {}
    results = await asyncio.gather(*tasks)
    results.append(search_result)

    for res in results:
        for key, value in res.items():
            data[key] = value

    return data


async def main_search(ticer: str, inline_search: bool = False) -> dict | bool:
    url = f'https://www.investing.com/search/?q={ticer}'
    parser = ParseInfo()

    async with aiohttp.ClientSession(headers=headers) as session:
        search_result = await get_parse_info(session, parser.search_ticer, url, ticer)

        if not search_result:
            return search_result

        if inline_search:
            return search_result

        return await get_all(session, parser, search_result, ticer)