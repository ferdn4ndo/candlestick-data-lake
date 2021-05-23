import os
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker

from app.models import Exchange


def show_help():
    return """
    Populates the initial exchange data.
    
    Usage:
    python manage.py populate_exchange_data <exchange_code> <pair_symbol>
    
    The available exchange codes are:
      binance
      
    To list the available pair symbols for a given exchange, run:
    python manage.py populate_exchange_data <exchange_code> --list-symbols
"""


def execute(arguments: list):
    if len(arguments) < 2:
        print(
            'This command expects two arguments: the exchange name and the pair symbol. Run with --help for more info.')
        return

    engine = create_engine(os.getenv("DATABASE_URL"))
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    exchange_code = arguments[1]
    try:
        exchange = session.query(Exchange).filter_by(code=exchange_code).one()
    except NoResultFound:
        print('Exchange code {} not found!'.format(exchange_code))
        return

    print('Selected exchange {} - {}'.format(exchange_code.code, exchange_code.name))

    print('We should be importing here..')
    # ToDo: instantiate the exchange service and import
