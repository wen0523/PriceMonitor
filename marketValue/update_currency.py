import logging
import requests
import ccxt
import yaml
import time

def loadConfig(configPath='config/config.yaml'):
    try:
        with open(configPath, 'r') as file:
            config = yaml.safe_load(file)
        required_keys = ['exchange', 'marketValue', 'symbolsFilePath']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")

        return config
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        raise

def get_coin_names():
    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url).json()
        for i, coin in enumerate(response):
            if i > 3:
                break
            else:
                print(coin)
        return {coin['symbol'].upper():coin['id'] for coin in response}
    except Exception as e:
        logging.error(f"Failed to fetch CoinGecko data1: {e}")

        return {}

def get_usdt_trading_pairs(exchange_name):
    # 初始化交易所实例
    exchange = getattr(ccxt, exchange_name)({
        'enableRateLimit': True,  # 启用速率限制
    })
    
    try:
        # 获取所有交易对信息
        markets = exchange.fetch_markets()
        
        # 筛选以 USDT 为报价货币的活跃交易对
        usdt_pairs = [
            market['symbol'].split('/')[0] for market in markets 
            if market['quote'].upper() == 'USDT' 
            and market.get('active', False)
        ]
        
        return usdt_pairs
    
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []

def get_coin_ids(usdt_pairs, names):
    coin_ids = []
    others = [] # Used to store coins whose market value cannot be obtained through CoinGecko

    for symbol in usdt_pairs:
        # 统一符号为大写匹配
        normalized_symbol = symbol.upper()
        if normalized_symbol in names:
            
            coin_ids.append(names[normalized_symbol].lower())
        else:
            others.append(symbol)

    return coin_ids, others

def get_coin_ranking(coin_ids):
    try:
        all_coins = []
        batch_size = 200  # CoinGecko 免费 API 单次最多 200 个 ID
        
        # 分批处理
        for i in range(0, len(coin_ids), batch_size):
            batch_ids = coin_ids[i:i+batch_size]
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'ids': ','.join(batch_ids),
                'order': 'market_cap_desc',
                'sparkline': 'false'
            }
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查 HTTP 错误
            all_coins.extend(response.json())
            time.sleep(20)

        return all_coins
    except Exception as e:
        logging.error(f"Failed to fetch CoinGecko data2: {e}")
        return []

def get_content(response, others, num):
    try:
        symbolContent = ''
        allContent = ''
        notice = ''  # 初始化 notice 变量

        # 处理未匹配币种的提示信息
        if len(others) > 0:
            notice = '以下币种未从 CoinGecko 获取市值，请手动处理:\n'
            others_str = ''
            for i, other in enumerate(others):
                if i % 5 == 0 and i != 0:
                    others_str += '\n'
                others_str += f"{other.ljust(10)}"
            notice += others_str + '\n' + '-'*50 + '\n'

        # 处理市值数据
        for i, coin in enumerate(response):
            name = coin.get('name', '未知币种')
            symbol = coin.get('symbol', '?').upper()
            market_cap = coin.get('market_cap', 0)  # 处理 None 值
            if i < num:
                symbolContent += f"{symbol}/USDT\n"
            allContent += f"{name} ({symbol}) 市值: ${market_cap:,.0f}\n"

        full_content = notice + allContent
        return symbolContent, full_content
    except Exception as e:
        logging.error(f"生成内容失败: {e}")
        return '', ''  # 返回两个空字符串

def write_file(exchange, symbolsFilePath, symbolContent, allContent):
    if allContent == '' or symbolContent == '':
        return
    try:
        with open('marketValue/' + exchange +'_ranking.txt', 'w', encoding="utf-8") as f:
            f.write(allContent)

        with open(symbolsFilePath + '/' + exchange+'_symbols.txt', 'w', encoding="utf-8") as f:
            f.write(symbolContent)
    except IOError as e:
        logging(e)


if __name__ == '__main__':
    config = loadConfig()

    names = get_coin_names()
    usdt_pairs = get_usdt_trading_pairs(config['exchange'])

    coin_ids, others = get_coin_ids(usdt_pairs, names)

    response = get_coin_ranking(coin_ids)
    print(len(response))
    num = config['marketValue'] if (len(usdt_pairs) - len(others)) >= config['marketValue'] else (len(usdt_pairs) - len(others))
    print(num)
    symbolContent, allContent = get_content(response, others, num)

    write_file(config['exchange'], config['symbolsFilePath'],symbolContent, allContent)


