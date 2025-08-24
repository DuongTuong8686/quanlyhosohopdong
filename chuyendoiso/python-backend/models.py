#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQLAlchemy models for CDS Scanner
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False, index=True)
    document_type = Column(String(100), nullable=True, index=True)
    extracted_text = Column(Text, nullable=True)
    processed_data = Column(Text, nullable=True)  # store JSON as text for MSSQL compatibility
    confidence = Column(String(50), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)


