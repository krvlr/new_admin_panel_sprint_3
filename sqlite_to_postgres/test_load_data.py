import logging
import os
from dataclasses import dataclass

import psycopg2
from dotenv import load_dotenv
from load_data import conn_context
from models_dataclasses import TABLE_NAME_DATACLASS_MAPPING
from psycopg2.extras import DictCursor
from settings import POSTGRES_CONNECTION_SETTINGS, SQLITE_DB_FILE

load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_rows_count(conn, table_name: str, schema: str = "") -> int:
    curs = conn.cursor()
    curs.execute(
        "SELECT count(*) FROM {schema}{table_name};".format(
            schema=schema, table_name=table_name
        )
    )
    return curs.fetchone()[0]


def get_all_data(conn, table_name: str, schema: str = "") -> list[dataclass]:
    curs = conn.cursor()
    curs.execute(
        "SELECT * FROM {schema}{table_name};".format(
            schema=schema, table_name=table_name
        )
    )
    db_rows = curs.fetchall()
    dataclass_list = []
    for row in db_rows:
        dataclass_list.append(
            TABLE_NAME_DATACLASS_MAPPING.get(table_name).from_dict(dict(row))
        )
    return dataclass_list


if __name__ == "__main__":
    with (
        conn_context(SQLITE_DB_FILE) as sqlite_conn,
        psycopg2.connect(
            **POSTGRES_CONNECTION_SETTINGS, cursor_factory=DictCursor
        ) as pg_conn,
    ):
        for table_name in TABLE_NAME_DATACLASS_MAPPING.keys():
            sqlite_count = get_rows_count(sqlite_conn, table_name)
            pg_count = get_rows_count(pg_conn, table_name, "content.")

            assert sqlite_count == pg_count, (
                f"Не совпадает количество записей в {table_name}: "
                + f"sqlite ({sqlite_count}) и postgresql ({pg_count})"
            )

            sqlite_table_data = get_all_data(sqlite_conn, table_name)
            pg_table_data = get_all_data(pg_conn, table_name, "content.")

            sqlite_data_hash_list = [
                hash(table_data) for table_data in sqlite_table_data
            ]
            pg_data_hash_list = [hash(table_data) for table_data in pg_table_data]

            for sqlite_data_hash in sqlite_data_hash_list:
                assert (
                    sqlite_data_hash in pg_data_hash_list
                ), "Отсутствует совпадение для объекта"

    logging.info("Тест на совпадение данных выполнился успешно!")
