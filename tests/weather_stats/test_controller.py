"""
Module to Test Weather Stats Controller Functionality
"""

from datetime import datetime, timedelta

import pytest
from fastapi.datastructures import QueryParams
from httpx import AsyncClient, Auth
from httpx import Request as httpx_request

from core import utils
from core.user import User
from weather.model import Weather

base_url = "/api/weather/stats"


@pytest.mark.asyncio
async def test_paginate(async_client: AsyncClient) -> None:
    response = await async_client.get(base_url, params=QueryParams(**{"page_size": 1}))
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["data"][0]["id"] is not None

    next_page = json_response["meta"]["next_page_link"]
    response = await async_client.get(next_page)

    assert response.status_code == 200
    json_response = response.json()

    assert json_response["data"][0]["id"] is not None


@pytest.mark.asyncio
async def test_paginate_station_name_filter_non_existing_item(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        base_url, params=QueryParams(**{"station_name": "NoneExistingItem"})
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["data"] == []


@pytest.mark.asyncio
async def test_paginate_station_name_filter_existing_item(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        base_url, params=QueryParams(**{"station_name": "USC00110072"})
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response["data"]) > 0


@pytest.mark.asyncio
async def test_paginate_measure_year_filter_non_existing_item(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        base_url, params=QueryParams(**{"measure_year": "2030"})
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response["data"]) == 0


@pytest.mark.asyncio
async def test_paginate_measure_year_filter_existing_item(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        base_url, params=QueryParams(**{"measure_year": "2000"})
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response["data"]) > 0


@pytest.mark.asyncio
async def test_paginate_station_name_measure_year_filter_existing_item(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(
        base_url,
        params=QueryParams(**{"measure_year": "2014", "station_name": "USC00110072"}),
    )
    assert response.status_code == 200
    json_response = response.json()
    assert len(json_response["data"]) == 1
    assert json_response["data"][0]["max_temperature"] == 138
    assert json_response["data"][0]["min_temperature"] == 24
    assert json_response["data"][0]["total_precipitation_cm"] == 986.3


@pytest.mark.asyncio
async def test_paginate_bad_measure_date_filter(async_client: AsyncClient) -> None:
    response = await async_client.get(
        base_url, params=QueryParams(**{"measure_year": "2030-01-"})
    )
    assert response.status_code == 422
