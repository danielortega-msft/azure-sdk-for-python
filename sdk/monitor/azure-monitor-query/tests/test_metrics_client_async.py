# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# -------------------------------------------------------------------------
from datetime import timedelta

import pytest

from azure.monitor.query import MetricAggregationType, Metric
from azure.monitor.query.aio import MetricsQueryClient
from devtools_testutils import AzureRecordedTestCase


METRIC_NAME = "Event"

class TestMetricsClientAsync(AzureRecordedTestCase):

    @pytest.mark.asyncio
    async def test_metrics_auth(self, recorded_test, monitor_info):
        client = self.create_client_from_credential(
            MetricsQueryClient, self.get_credential(MetricsQueryClient, is_async=True))
        async with client:
            response = await client.query_resource(
                monitor_info['metrics_resource_id'],
                metric_names=[METRIC_NAME],
                timespan=timedelta(days=1),
                aggregations=[MetricAggregationType.COUNT]
                )
            assert response
            assert response.metrics

    @pytest.mark.asyncio
    async def test_metrics_granularity(self, recorded_test, monitor_info):
        client = self.create_client_from_credential(
            MetricsQueryClient, self.get_credential(MetricsQueryClient, is_async=True))
        async with client:
            response = await client.query_resource(
                monitor_info['metrics_resource_id'],
                metric_names=[METRIC_NAME],
                timespan=timedelta(days=1),
                granularity=timedelta(minutes=5),
                aggregations=[MetricAggregationType.COUNT]
                )
            assert response
            assert response.granularity == timedelta(minutes=5)

    @pytest.mark.asyncio
    async def test_metrics_filter(self, recorded_test, monitor_info):
        client = self.create_client_from_credential(
            MetricsQueryClient, self.get_credential(MetricsQueryClient, is_async=True))
        async with client:
            response = await client.query_resource(
                monitor_info['metrics_resource_id'],
                metric_names=[METRIC_NAME],
                timespan=timedelta(days=1),
                granularity=timedelta(minutes=5),
                filter="Source eq '*'",
                aggregations=[MetricAggregationType.COUNT]
                )
            assert response
            metric = response.metrics[METRIC_NAME]
            for t in metric.timeseries:
                assert t.metadata_values is not None

    @pytest.mark.asyncio
    async def test_metrics_list(self, recorded_test, monitor_info):
        client = self.create_client_from_credential(
            MetricsQueryClient, self.get_credential(MetricsQueryClient, is_async=True))
        async with client:
            response = await client.query_resource(
                monitor_info['metrics_resource_id'],
                metric_names=[METRIC_NAME],
                timespan=timedelta(days=1),
                granularity=timedelta(minutes=5),
                aggregations=[MetricAggregationType.COUNT]
                )
            assert response
            metrics = response.metrics
            assert len(metrics) == 1
            assert metrics[0].__class__ == Metric
            assert metrics[METRIC_NAME].__class__ == Metric
            assert metrics[METRIC_NAME] == metrics[0]

    @pytest.mark.asyncio
    async def test_metrics_namespaces(self, recorded_test, monitor_info):
        client = self.create_client_from_credential(
            MetricsQueryClient, self.get_credential(MetricsQueryClient, is_async=True))

        async with client:
            response = client.list_metric_namespaces(monitor_info['metrics_resource_id'])

            assert response is not None
            async for item in response:
                assert item

    @pytest.mark.asyncio
    async def test_metrics_definitions(self, recorded_test, monitor_info):
        client = self.create_client_from_credential(
            MetricsQueryClient, self.get_credential(MetricsQueryClient, is_async=True))

        async with client:
            response = client.list_metric_definitions(
                monitor_info['metrics_resource_id'], namespace='Microsoft.OperationalInsights/workspaces')

            assert response is not None
            async for item in response:
                assert item
