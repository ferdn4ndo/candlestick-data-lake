from tornado_sqlalchemy import SessionMixin, as_future

from app import __version__
from app.controllers.base_controller import BaseController
from app.models import Candlestick, Currency, CurrencyPair, Exchange


class HealthController(BaseController, SessionMixin):
    async def get(self):
        with self.make_session() as session:
            total_candlesticks = await as_future(session.query(Candlestick).count)
            total_currencies = await as_future(session.query(Currency).count)
            total_currency_pairs = await as_future(session.query(CurrencyPair).count)
            total_exchanges = await as_future(session.query(Exchange).count)

        self.write(
            {
                "system": {
                    "name": "candlestick-data-lake",
                    "version": __version__,
                    "github": "https://github.com/ferdn4ndo/candlestick-data-lake/",
                },
                "database": {
                    "candlesticks": total_candlesticks,
                    "currencies": total_currencies,
                    "currencyPairs": total_currency_pairs,
                    "exchanges": total_exchanges,
                },
                "services": {
                    "binance": {
                        "status": "ToDo",
                    }
                },
            }
        )
