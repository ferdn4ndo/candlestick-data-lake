import logging

from sqlalchemy.orm import Session

from app.services.consumer_service_factory import create_client_from_exchange_code, create_service_from_exchange_code
from app.services.exchanges.exchange_service_factory import get_exchange_by_code


class SetupService:
    def setUpExchange(session: Session, exchange_code: str):
        exchange = get_exchange_by_code(session=session, exchange_code=exchange_code)
        exchange_client = create_client_from_exchange_code(exchange_code=exchange_code)
        exchange_service = create_service_from_exchange_code(exchange_code=exchange_code)

        symbols = exchange_client.get_symbols()
        for symbol in symbols:
            logging.info(f"Configuring symbol {symbol}")

            currency_base = exchange_service.add_currency(symbol["currencyBase"])
            currency_quote = exchange_service.add_currency(symbol["currencyQuote"])

            exchange_service.add_currency_pair(session, exchange, symbol["symbol"], currency_base, currency_quote)

            session.commit()

        logging.info(f"Finished setting up {len(symbols)} symbols!")
