#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database helpers for CDS Scanner (SQLAlchemy engine/session setup)
Supports SQL Server via pyodbc with Windows Authentication by default
"""

from __future__ import annotations

import contextlib
from typing import Optional
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_CONFIG


def _build_mssql_connection_url() -> str:
    """Build SQLAlchemy connection URL for SQL Server using pyodbc.

    Priority: Windows Authentication (Trusted Connection) unless username provided.
    """
    server = DATABASE_CONFIG.get("host", "localhost")
    database = DATABASE_CONFIG.get("database", "CDS")
    username = DATABASE_CONFIG.get("username") or ""
    password = DATABASE_CONFIG.get("password") or ""
    driver = DATABASE_CONFIG.get("driver") or "ODBC Driver 17 for SQL Server"
    trust_cert = DATABASE_CONFIG.get("trust_server_certificate", True)
    trusted_conn = DATABASE_CONFIG.get("trusted_connection", True)

    # Encode driver and params
    driver_q = quote_plus(driver)

    if username and password:
        return (
            f"mssql+pyodbc://{quote_plus(username)}:{quote_plus(password)}@{server}/{database}"
            f"?driver={driver_q}&TrustServerCertificate={'yes' if trust_cert else 'no'}"
        )

    # Windows Authentication (Trusted_Connection)
    return (
        f"mssql+pyodbc://@{server}/{database}?driver={driver_q}"
        f"&Trusted_Connection={'Yes' if trusted_conn else 'No'}"
        f"&TrustServerCertificate={'yes' if trust_cert else 'no'}"
    )


def build_connection_url() -> Optional[str]:
    db_type = DATABASE_CONFIG.get("type", "sqlite").lower()
    if db_type in {"mssql", "sqlserver", "sql_server"}:
        return _build_mssql_connection_url()
    elif db_type == "sqlite":
        sqlite_path = DATABASE_CONFIG.get("sqlite_path")
        return f"sqlite:///{sqlite_path}"
    return None


def create_db_engine(echo: bool = False) -> Engine:
    url = build_connection_url()
    if not url:
        raise RuntimeError("DATABASE_CONFIG is not properly configured")
    # For MSSQL + pyodbc, use fast_executemany when available
    engine = create_engine(url, echo=echo, pool_pre_ping=True, future=True)
    return engine


def ensure_database_exists(engine: Engine) -> None:
    """Ensure database exists for MSSQL. If target DB cannot be opened,
    try to create it by connecting to 'master' and issuing CREATE DATABASE.
    Requires permissions; otherwise it's a no-op.
    """
    db_type = DATABASE_CONFIG.get("type", "sqlite").lower()
    if db_type not in {"mssql", "sqlserver", "sql_server"}:
        return

    database = DATABASE_CONFIG.get("database", "CDS")

    # Try a simple query; if it fails with cannot open DB, attempt create
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return
    except Exception:
        pass

    # Connect to master and create database
    try:
        server = DATABASE_CONFIG.get("host", "localhost")
        driver = DATABASE_CONFIG.get("driver") or "ODBC Driver 17 for SQL Server"
        username = DATABASE_CONFIG.get("username") or ""
        password = DATABASE_CONFIG.get("password") or ""
        trust_cert = DATABASE_CONFIG.get("trust_server_certificate", True)
        trusted_conn = DATABASE_CONFIG.get("trusted_connection", True)

        driver_q = quote_plus(driver)
        if username and password:
            master_url = (
                f"mssql+pyodbc://{quote_plus(username)}:{quote_plus(password)}@{server}/master"
                f"?driver={driver_q}&TrustServerCertificate={'yes' if trust_cert else 'no'}"
            )
        else:
            master_url = (
                f"mssql+pyodbc://@{server}/master?driver={driver_q}"
                f"&Trusted_Connection={'Yes' if trusted_conn else 'No'}"
                f"&TrustServerCertificate={'yes' if trust_cert else 'no'}"
            )

        with create_engine(master_url, pool_pre_ping=True, future=True).connect() as conn:
            conn.execute(text(f"IF DB_ID('{database}') IS NULL CREATE DATABASE [{database}]"))
            conn.commit()
    except Exception:
        # Ignore if no permission; server will error later when used
        pass


# Create a shared engine and session factory if DB is enabled
ENGINE: Optional[Engine] = None
SessionLocal = None

if DATABASE_CONFIG.get("enabled"):
    ENGINE = create_db_engine(echo=DATABASE_CONFIG.get("echo", False))
    ensure_database_exists(ENGINE)
    SessionLocal = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False, future=True)


@contextlib.contextmanager
def db_session():
    if SessionLocal is None:
        raise RuntimeError("Database is not enabled or not configured")
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


