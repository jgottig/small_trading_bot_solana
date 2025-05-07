
# Solana Swap by Solana Tracker

How does it work?

The bot monitors the Telegram Calls group of your choice. Once inside, every time a buy alert is sent in the group for a specific coin, the bot retrieves its Market Cap and contract address. If both meet the established conditions, the purchase is executed automatically.

Then, the bot continues to monitor the coin’s price, using different percentage thresholds based on the current price to decide whether to sell or hold. If the Market Cap increases, the bot automatically updates the sell range (floor price).

If the Market Cap drops below the sell floor (Stop Loss), the bot executes the sell order automatically and continues monitoring.

- Choose your Telegram channel
- Assign your Telegram ID and credentials
- Assign your Solana address

Run and fun

Uses the Solana Swap api from [https://docs.solanatracker.io](https://docs.solanatracker.io)

## UPDATE - July 9: Swap API has been updated, way faster and supporting new markets!

## Now supporting
- Raydium
- Raydium CPMM
- Pump.fun
- Moonshot
- Orca
- Jupiter (Private Self Hosted API)

## Installation

```bash
git clone https://github.com/YZYLAB/small_bot_trading.git
```

## Demo

Swap API is used live on:
https://www.solanatracker.io
