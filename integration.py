import asyncio
import unittest
import requests
import psycopg2
from time import sleep
import json
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

sys.path.append(str(BASE_DIR / 'generatepass_service/app'))
sys.path.append(str(BASE_DIR / 'user_service/app'))

from generatepass_service.app.main import generatepass_health as health_generatepass
from user_service.app.main import user_health as health_user

def check_connect():
    try:
        conn = psycopg2.connect(
            dbname='Pavlovid',
            user='ilya',
            password='pavlov',
            host='localhost',
            port='5432'
        )
        conn.close()
        return True
    except Exception as e:
        return False


class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_db_connection(self):
        sleep(5)
        self.assertEqual(check_connect(), True)

    def test_generatepass_service_connection(self):
        r = asyncio.run(health_generatepass())
        self.assertEqual(r, {'message': 'service is active'})

    def test_user_service_connection(self):
        r = asyncio.run(health_user())
        self.assertEqual(r, {'message': 'service is active'})


if __name__ == '__main__':
    unittest.main()
