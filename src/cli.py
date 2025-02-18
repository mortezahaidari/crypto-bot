# src/cli.py
import argparse
from src.core.bot import CryptoBot
from src.data.backtester import Backtester
from src.strategies import MovingAverageCrossover

def main():
    parser = argparse.ArgumentParser(description="Crypto Trading Bot CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Start the bot
    start_parser = subparsers.add_parser("start", help="Start the trading bot")
    start_parser.add_argument("--config", default="config/config.yaml", help="Path to config file")

    # Run a backtest
    backtest_parser = subparsers.add_parser("backtest", help="Run a backtest")
    backtest_parser.add_argument("--strategy", required=True, help="Strategy to test (e.g., moving_average)")
    backtest_parser.add_argument("--data", required=True, help="Path to historical data CSV")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "start":
        bot = CryptoBot(config_path=args.config)
        bot.run()
    elif args.command == "backtest":
        backtester = Backtester(strategy=MovingAverageCrossover())
        data = pd.read_csv(args.data)
        report = backtester.run(data)
        print(report)

if __name__ == "__main__":
    main()