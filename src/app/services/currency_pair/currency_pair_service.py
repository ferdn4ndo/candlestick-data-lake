import logging

from datetime import datetime
from sqlalchemy.orm import Session

from app.errors import ResourceNotInUseError, ResourceNotFoundError
from app.errors.resource_already_in_use_error import ResourceAlreadyInUseError
from app.models import CurrencyPair, Exchange
from app.services.temp_file_service import check_if_temp_file_exists, remove_temp_file, save_temp_file, FileMode


class CurrencyPairService:
    def __init__(self, currency_pair: CurrencyPair):
        self.currency_pair = currency_pair

    @staticmethod
    def check_if_symbol_exists(session: Session, exchange: Exchange, symbol: str) -> None:
        currency_pair = session.query(CurrencyPair).filter_by(exchange=exchange, symbol=symbol).first()
        if currency_pair is None:
            raise ResourceNotFoundError(f"The pair symbol '{symbol}' was not found in exchange '{exchange.code}'!")

    @staticmethod
    def get_lock_filename(pair_symbol: str, exchange_code: str, agent: str) -> str:
        return f"lock_{agent}_{exchange_code}_{pair_symbol}.lock"

    @staticmethod
    def is_in_use(pair_symbol: str, exchange_code: str, agent: str = "default") -> bool:
        lock_filename = CurrencyPairService.get_lock_filename(
            pair_symbol=pair_symbol, exchange_code=exchange_code, agent=agent
        )

        temp_file_exists = 1 if check_if_temp_file_exists(lock_filename) else 0

        logging.info(f"Checking if has lock for pair {pair_symbol} from exchange {exchange_code} (agent: {agent})")
        logging.info(f"Lock temp file: {lock_filename} | Exists: {temp_file_exists}")

        return check_if_temp_file_exists(lock_filename)

    @staticmethod
    def set_in_use(
        pair_symbol: str, exchange_code: str, agent: str = "default", raise_error: bool = True, file_content: str = ""
    ):
        in_use = CurrencyPairService.is_in_use(pair_symbol=pair_symbol, exchange_code=exchange_code, agent=agent)
        if raise_error and in_use:
            raise ResourceNotInUseError(
                f"The pair '{pair_symbol}' from exchange code '{exchange_code}' is already in use!"
            )

        if not in_use:
            lock_filename = CurrencyPairService.get_lock_filename(
                pair_symbol=pair_symbol,
                exchange_code=exchange_code,
                agent=agent,
            )
            save_temp_file(
                filename=lock_filename, content=file_content, filemode=FileMode.FILE_MODE_CREATE_ERROR_IF_EXISTS
            )

    @staticmethod
    def reset_in_use(pair_symbol: str, exchange_code: str, agent: str = "default", raise_error: bool = True):
        in_use = CurrencyPairService.is_in_use(
            pair_symbol=pair_symbol,
            exchange_code=exchange_code,
            agent=agent,
        )
        if raise_error and not in_use:
            raise ResourceNotInUseError(
                f"The pair '{pair_symbol}' from exchange code '{exchange_code}' is not being used!"
            )

        if in_use:
            lock_filename = CurrencyPairService.get_lock_filename(
                pair_symbol=pair_symbol,
                exchange_code=exchange_code,
                agent=agent,
            )
            remove_temp_file(lock_filename)

    @staticmethod
    def check_in_use(agent: str, exchange_code: str, symbol: str):
        in_use = CurrencyPairService.is_in_use(agent=agent, pair_symbol=symbol, exchange_code=exchange_code)

        if in_use:
            raise ResourceAlreadyInUseError(
                f"The pair symbol '{symbol}' is already being fetched from '{exchange_code}'."
            )

        CurrencyPairService.set_in_use(
            pair_symbol=symbol,
            exchange_code=exchange_code,
            agent=agent,
            raise_error=True,
            file_content=datetime.now().isoformat(),
        )
