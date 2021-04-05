from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from .models import Fund, Holding, Trades


def get_etf_profile(db: Session, symbol: str):
    if symbol:
        return db.query(Fund).filter(Fund.symbol == symbol).all()
    else:
        return db.query(Fund).all()


def get_etf_holdings(db: Session, symbol: str, holding_date: str):
    return (
        db.query(Holding)
        .filter(Holding.fund == symbol, Holding.date == holding_date)
        .all()
    )


def get_etf_holdings_maxdate(db: Session, symbol: str):
    return (
        db.query(func.max(Holding.date).label("date"))
        .filter(Holding.fund == symbol)
        .one()
    )


def get_etf_trades(db: Session, symbol: str, start_date: str, end_date: str):
    return (
        db.query(Trades)
        .filter(
            Trades.fund == symbol, Trades.date >= start_date, Trades.date <= end_date
        )
        .all()
    )


def get_etf_trades_dates(db: Session, symbol: str):
    return (
        db.query(
            func.min(Trades.date).label("mindate"),
            func.max(Trades.date).label("maxdate"),
        )
        .filter(Trades.fund == symbol)
        .one()
    )


def get_etf_trades_maxdate(db: Session):
    return (
        db.query(
            func.max(Trades.date).label("maxdate"),
        ).one()
    )[0]


def get_stock_fundownership(db: Session, symbol: str):
    subq = (
        db.query(Holding.fund, func.max(Holding.date).label("maxdate"))
        .group_by(Holding.fund)
        .subquery("t2")
    )

    return (
        db.query(Holding)
        .join(subq, and_(Holding.date == subq.c.maxdate))
        .filter(Holding.ticker == symbol)
        .all()
    )


def get_stock_fundownership_maxdate(db: Session, symbol: str):
    return (
        db.query(func.max(Holding.date).label("maxdate"))
        .filter(Holding.ticker == symbol)
        .first()
    )[0]


def get_stock_trades(db: Session, symbol: str, direction: str):
    if direction:
        return (
            db.query(Trades)
            .filter(Trades.ticker == symbol, Trades.direction == direction.capitalize())
            .order_by(Trades.date.desc(), Trades.fund)
            .all()
        )
    else:
        return (
            db.query(Trades)
            .filter(Trades.ticker == symbol)
            .order_by(Trades.date.desc(), Trades.fund)
            .all()
        )


def get_stock_trades_dates(db: Session, symbol: str):
    return (
        db.query(
            func.min(Trades.date).label("mindate"),
            func.max(Trades.date).label("maxdate"),
        )
        .filter(Trades.ticker == symbol)
        .one()
    )
