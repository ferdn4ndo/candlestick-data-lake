import logging
import os

from sqlalchemy.orm import Session

from app.errors import ResourceNotInUseError, ResourceNotFoundError
from app.models import CurrencyPair, Exchange
from app.services.temp_file_service import check_if_temp_file_exists, remove_temp_file, save_temp_file, FileMode


class CurrencyPairService:
    def __init__(self, currency_pair: CurrencyPair):
        self.currency_pair = currency_pair

    @staticmethod
    def check_if_symbol_exists(session: Session, exchange: Exchange, symbol: str) -> None:
        symbol = session.query(CurrencyPair).filter_by(exchange=exchange, symbol=symbol).first()
        if symbol is None:
            raise ResourceNotFoundError(f"The pair symbol '{symbol}' was not found in exchange'{exchange.code}'!")

    @staticmethod
    def get_lock_filename(pair_symbol: str, exchange_code: str, agent: str) -> str:
        return f"lock_{agent}_{exchange_code}_{pair_symbol}.lock"

    @staticmethod
    def is_in_use(pair_symbol: str, exchange_code: str, agent: str = "default") -> bool:
        lock_filename = CurrencyPairService.get_lock_filename(
            pair_symbol=pair_symbol,
            exchange_code=exchange_code,
            agent=agent
        )

        tempFileExists = 1 if check_if_temp_file_exists(lock_filename) else 0

        logging.info(f"Checking if has lock for pair {pair_symbol} from exchange {exchange_code} (agent: {agent})")
        logging.info(f"Lock temp file: {lock_filename} | Exists: {tempFileExists}")

        return check_if_temp_file_exists(lock_filename)

    @staticmethod
    def set_in_use(
            pair_symbol: str,
            exchange_code: str,
            agent: str = "default",
            raise_error: bool = True,
            file_content: str = ""
    ):
        in_use = CurrencyPairService.is_in_use(
            pair_symbol=pair_symbol,
            exchange_code=exchange_code,
            agent=agent
        )
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
                filename=lock_filename,
                content=file_content,
                filemode=FileMode.FILE_MODE_CREATE_ERROR_IF_EXISTS
            )

    @staticmethod
    def reset_in_use(
            pair_symbol: str,
            exchange_code: str,
            agent: str = "default",
            raise_error: bool = True
    ):
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
