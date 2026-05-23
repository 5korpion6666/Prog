# test_lab6.py

import pytest
from unittest.mock import patch, MagicMock
from lab6_rare import exchange_rates_generator, rate_pairs_generator


# ─────────────────────────────────────────────
# Фикстуры
# ─────────────────────────────────────────────

MOCK_USD_RESPONSE = {
    'base_code': 'USD',
    'rates': {'RUB': 90.5, 'EUR': 0.92, 'GBP': 0.79, 'JPY': 149.5, 'CNY': 7.24}
}

MOCK_EUR_RESPONSE = {
    'base_code': 'EUR',
    'rates': {'RUB': 98.3, 'USD': 1.09, 'GBP': 0.86, 'JPY': 162.1, 'CNY': 7.88}
}


def make_mock_response(data):
    mock = MagicMock()
    mock.json.return_value = data
    mock.raise_for_status.return_value = None
    return mock


# ─────────────────────────────────────────────
# Тесты exchange_rates_generator
# ─────────────────────────────────────────────

class TestExchangeRatesGenerator:
    def test_returns_base_and_rates(self):
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.return_value = make_mock_response(MOCK_USD_RESPONSE)
            results = list(exchange_rates_generator(['USD']))
        assert results[0]['base'] == 'USD'
        assert 'rates' in results[0]

    def test_yields_multiple_currencies(self):
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.side_effect = [
                make_mock_response(MOCK_USD_RESPONSE),
                make_mock_response(MOCK_EUR_RESPONSE),
            ]
            results = list(exchange_rates_generator(['USD', 'EUR']))
        assert len(results) == 2
        assert results[0]['base'] == 'USD'
        assert results[1]['base'] == 'EUR'

    def test_yields_error_on_failure(self):
        import requests as req
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.side_effect = req.exceptions.RequestException('Timeout')
            results = list(exchange_rates_generator(['USD']))
        assert 'error' in results[0]
        assert results[0]['base'] == 'USD'

    def test_is_generator(self):
        import types
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.return_value = make_mock_response(MOCK_USD_RESPONSE)
            gen = exchange_rates_generator(['USD'])
        assert isinstance(gen, types.GeneratorType)

    def test_empty_input(self):
        results = list(exchange_rates_generator([]))
        assert results == []

    def test_rates_contain_rub(self):
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.return_value = make_mock_response(MOCK_USD_RESPONSE)
            results = list(exchange_rates_generator(['USD']))
        assert 'RUB' in results[0]['rates']


# ─────────────────────────────────────────────
# Тесты rate_pairs_generator
# ─────────────────────────────────────────────

class TestRatePairsGenerator:
    def test_returns_correct_pair(self):
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.return_value = make_mock_response(MOCK_USD_RESPONSE)
            results = list(rate_pairs_generator([('USD', 'RUB')]))
        assert results[0]['from'] == 'USD'
        assert results[0]['to'] == 'RUB'
        assert results[0]['rate'] == 90.5

    def test_yields_multiple_pairs(self):
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.side_effect = [
                make_mock_response(MOCK_USD_RESPONSE),
                make_mock_response(MOCK_EUR_RESPONSE),
            ]
            results = list(rate_pairs_generator([('USD', 'RUB'), ('EUR', 'RUB')]))
        assert len(results) == 2

    def test_error_on_unknown_currency(self):
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.return_value = make_mock_response(MOCK_USD_RESPONSE)
            results = list(rate_pairs_generator([('USD', 'XYZ')]))
        assert 'error' in results[0]

    def test_error_on_request_failure(self):
        import requests as req
        with patch('lab6_rare.requests.get') as mock_get:
            mock_get.side_effect = req.exceptions.RequestException('Timeout')
            results = list(rate_pairs_generator([('USD', 'RUB')]))
        assert 'error' in results[0]

    def test_empty_input(self):
        results = list(rate_pairs_generator([]))
        assert results == []
