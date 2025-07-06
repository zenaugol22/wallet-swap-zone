"""
UTXO Auditor — утилита для анализа всех непотраченных выходов (UTXO) адреса.
"""

import requests
import sys

def get_utxos(address):
    url = f"https://blockstream.info/api/address/{address}/utxo"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def satoshi_to_btc(sat):
    return sat / 1e8

def main(address):
    print(f"🔎 Аудит UTXO адреса: {address}")
    try:
        utxos = get_utxos(address)
    except Exception as e:
        print("❌ Ошибка при получении UTXO:", e)
        return

    if not utxos:
        print("✅ Все средства потрачены. Нет UTXO.")
        return

    total = 0
    print(f"🔢 Найдено {len(utxos)} UTXO:")
    for utxo in utxos:
        value_btc = satoshi_to_btc(utxo['value'])
        total += value_btc
        print(f" - TXID: {utxo['txid']} | vout: {utxo['vout']} | Сумма: {value_btc:.8f} BTC")

    print(f"
💰 Общая сумма: {total:.8f} BTC")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python utxo_auditor.py <bitcoin_address>")
        sys.exit(1)
    main(sys.argv[1])
