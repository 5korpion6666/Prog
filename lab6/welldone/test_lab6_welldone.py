# test_lab6_welldone.py

import pytest
import types
from unittest.mock import patch, MagicMock
from lab6_welldone import exchange_rates_generator, exchange_rates_generator_threaded


MOCK_RATES = {
    'USD': {'base_code': 'USD', 'rates': {'RUB': 90.5, 'EUR': 0.92}},
    'EUR': {'base_code': 'EUR', 'rates': {'RUB': 98.3, 'USD': 1.09}},
    'GBP': {'base_code': 'GBP', 'rates': {'RUB': 95.7, 'USD': 1.27}},
}


def make_mock_response(currency):
    mock = MagicMock()
    mock.json.return_value = MOCK_RATES[currency]
    mock.raise_for_status.return_value = None
    return mock


class TestSingleThreaded:
    def test_is_generator(self):
        with patch('lab6_welldone.requests.get') as mock_get:
            mock_get.return_value = make_mock_response('USD')
            gen = exchange_rates_generator(['USD'])
        assert isinstance(gen, types.GeneratorType)

    def test_returns_correct_data(self):
        with patch('lab6_welldone.requests.get') as mock_get:
            mock_get.return_value = make_mock_response('USD')
            results = list(exchange_rates_generator(['USD']))
        assert results[0]['base'] == 'USD'
        assert results[0]['rates']['RUB'] == 90.5

    def test_error_handling(self):
        import requests as req
        with patch('lab6_welldone.requests.get') as mock_get:
            mock_get.side_effect = req.exceptions.RequestException('Timeout')
            results = list(exchange_rates_generator(['USD']))
        assert 'error' in results[0]

    def test_empty_input(self):
        assert list(exchange_rates_generator([])) == []


class TestMultiThreaded:
    def test_is_generator(self):
        with patch('lab6_welldone.requests.get') as mock_get:
            mock_get.return_value = make_mock_response('USD')
            gen = exchange_rates_generator_threaded(['USD'])
        assert isinstance(gen, types.GeneratorType)

    def test_returns_all_results(self):
        def side_effect(url, **kwargs):
            for currency in MOCK_RATES:
                if currency in url:
                    return make_mock_response(currency)
        with patch('lab6_welldone.requests.get', side_effect=side_effect):
            results = list(exchange_rates_generator_threaded(['USD', 'EUR', 'GBP']))
        assert len(results) == 3

    def test_error_handling(self):
        import requests as req
        with patch('lab6_welldone.requests.get') as mock_get:
            mock_get.side_effect = req.exceptions.RequestException('Timeout')
            results = list(exchange_rates_generator_threaded(['USD']))
        assert 'error' in results[0]

    def test_empty_input(self):
        assert list(exchange_rates_generator_threaded([])) == []

    def test_same_count_as_single(self):
        def side_effect(url, **kwargs):
            for currency in MOCK_RATES:
                if currency in url:
                    return make_mock_response(currency)
        currencies = ['USD', 'EUR', 'GBP']
        with patch('lab6_welldone.requests.get', side_effect=side_effect):
            single = list(exchange_rates_generator(currencies))
        with patch('lab6_welldone.requests.get', side_effect=side_effect):
            threaded = list(exchange_rates_generator_threaded(currencies))
        assert len(single) == len(threaded)
