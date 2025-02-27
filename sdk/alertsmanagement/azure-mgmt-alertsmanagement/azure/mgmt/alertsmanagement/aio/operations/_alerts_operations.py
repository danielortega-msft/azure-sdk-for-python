# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, AsyncIterable, Callable, Dict, Optional, TypeVar, Union

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._alerts_operations import (
    build_change_state_request,
    build_get_all_request,
    build_get_by_id_request,
    build_get_history_request,
    build_get_summary_request,
    build_meta_data_request,
)

T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]


class AlertsOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.alertsmanagement.aio.AlertsManagementClient`'s
        :attr:`alerts` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")

    @distributed_trace_async
    async def meta_data(self, identifier: Union[str, "_models.Identifier"], **kwargs: Any) -> _models.AlertsMetaData:
        """List alerts meta data information based on value of identifier parameter.

        :param identifier: Identification of the information to be retrieved by API call.
         "MonitorServiceList" Required.
        :type identifier: str or ~azure.mgmt.alertsmanagement.models.Identifier
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: AlertsMetaData or the result of cls(response)
        :rtype: ~azure.mgmt.alertsmanagement.models.AlertsMetaData
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.AlertsMetaData]

        request = build_meta_data_request(
            identifier=identifier,
            api_version=api_version,
            template_url=self.meta_data.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponseAutoGenerated, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("AlertsMetaData", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    meta_data.metadata = {"url": "/providers/Microsoft.AlertsManagement/alertsMetaData"}  # type: ignore

    @distributed_trace
    def get_all(
        self,
        target_resource: Optional[str] = None,
        target_resource_type: Optional[str] = None,
        target_resource_group: Optional[str] = None,
        monitor_service: Optional[Union[str, "_models.MonitorService"]] = None,
        monitor_condition: Optional[Union[str, "_models.MonitorCondition"]] = None,
        severity: Optional[Union[str, "_models.Severity"]] = None,
        alert_state: Optional[Union[str, "_models.AlertState"]] = None,
        alert_rule: Optional[str] = None,
        smart_group_id: Optional[str] = None,
        include_context: Optional[bool] = None,
        include_egress_config: Optional[bool] = None,
        page_count: Optional[int] = None,
        sort_by: Optional[Union[str, "_models.AlertsSortByFields"]] = None,
        sort_order: Optional[Union[str, "_models.SortOrder"]] = None,
        select: Optional[str] = None,
        time_range: Optional[Union[str, "_models.TimeRange"]] = None,
        custom_time_range: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncIterable["_models.Alert"]:
        """List all existing alerts, where the results can be filtered on the basis of multiple parameters
        (e.g. time range). The results can then be sorted on the basis specific fields, with the
        default being lastModifiedDateTime.

        :param target_resource: Filter by target resource( which is full ARM ID) Default value is
         select all. Default value is None.
        :type target_resource: str
        :param target_resource_type: Filter by target resource type. Default value is select all.
         Default value is None.
        :type target_resource_type: str
        :param target_resource_group: Filter by target resource group name. Default value is select
         all. Default value is None.
        :type target_resource_group: str
        :param monitor_service: Filter by monitor service which generates the alert instance. Default
         value is select all. Known values are: "Application Insights", "ActivityLog Administrative",
         "ActivityLog Security", "ActivityLog Recommendation", "ActivityLog Policy", "ActivityLog
         Autoscale", "Log Analytics", "Nagios", "Platform", "SCOM", "ServiceHealth", "SmartDetector",
         "VM Insights", and "Zabbix". Default value is None.
        :type monitor_service: str or ~azure.mgmt.alertsmanagement.models.MonitorService
        :param monitor_condition: Filter by monitor condition which is either 'Fired' or 'Resolved'.
         Default value is to select all. Known values are: "Fired" and "Resolved". Default value is
         None.
        :type monitor_condition: str or ~azure.mgmt.alertsmanagement.models.MonitorCondition
        :param severity: Filter by severity.  Default value is select all. Known values are: "Sev0",
         "Sev1", "Sev2", "Sev3", and "Sev4". Default value is None.
        :type severity: str or ~azure.mgmt.alertsmanagement.models.Severity
        :param alert_state: Filter by state of the alert instance. Default value is to select all.
         Known values are: "New", "Acknowledged", and "Closed". Default value is None.
        :type alert_state: str or ~azure.mgmt.alertsmanagement.models.AlertState
        :param alert_rule: Filter by specific alert rule.  Default value is to select all. Default
         value is None.
        :type alert_rule: str
        :param smart_group_id: Filter the alerts list by the Smart Group Id. Default value is none.
         Default value is None.
        :type smart_group_id: str
        :param include_context: Include context which has contextual data specific to the monitor
         service. Default value is false'. Default value is None.
        :type include_context: bool
        :param include_egress_config: Include egress config which would be used for displaying the
         content in portal.  Default value is 'false'. Default value is None.
        :type include_egress_config: bool
        :param page_count: Determines number of alerts returned per page in response. Permissible value
         is between 1 to 250. When the "includeContent"  filter is selected, maximum value allowed is
         25. Default value is 25. Default value is None.
        :type page_count: int
        :param sort_by: Sort the query results by input field,  Default value is
         'lastModifiedDateTime'. Known values are: "name", "severity", "alertState", "monitorCondition",
         "targetResource", "targetResourceName", "targetResourceGroup", "targetResourceType",
         "startDateTime", and "lastModifiedDateTime". Default value is None.
        :type sort_by: str or ~azure.mgmt.alertsmanagement.models.AlertsSortByFields
        :param sort_order: Sort the query results order in either ascending or descending.  Default
         value is 'desc' for time fields and 'asc' for others. Known values are: "asc" and "desc".
         Default value is None.
        :type sort_order: str or ~azure.mgmt.alertsmanagement.models.SortOrder
        :param select: This filter allows to selection of the fields(comma separated) which would  be
         part of the essential section. This would allow to project only the  required fields rather
         than getting entire content.  Default is to fetch all the fields in the essentials section.
         Default value is None.
        :type select: str
        :param time_range: Filter by time range by below listed values. Default value is 1 day. Known
         values are: "1h", "1d", "7d", and "30d". Default value is None.
        :type time_range: str or ~azure.mgmt.alertsmanagement.models.TimeRange
        :param custom_time_range: Filter by custom time range in the format
         :code:`<start-time>`/:code:`<end-time>`  where time is in (ISO-8601 format)'. Permissible
         values is within 30 days from  query time. Either timeRange or customTimeRange could be used
         but not both. Default is none. Default value is None.
        :type custom_time_range: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either Alert or the result of cls(response)
        :rtype: ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.alertsmanagement.models.Alert]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.AlertsList]

        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop("error_map", {}) or {})

        def prepare_request(next_link=None):
            if not next_link:

                request = build_get_all_request(
                    subscription_id=self._config.subscription_id,
                    target_resource=target_resource,
                    target_resource_type=target_resource_type,
                    target_resource_group=target_resource_group,
                    monitor_service=monitor_service,
                    monitor_condition=monitor_condition,
                    severity=severity,
                    alert_state=alert_state,
                    alert_rule=alert_rule,
                    smart_group_id=smart_group_id,
                    include_context=include_context,
                    include_egress_config=include_egress_config,
                    page_count=page_count,
                    sort_by=sort_by,
                    sort_order=sort_order,
                    select=select,
                    time_range=time_range,
                    custom_time_range=custom_time_range,
                    api_version=api_version,
                    template_url=self.get_all.metadata["url"],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore

            else:
                request = HttpRequest("GET", next_link)
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("AlertsList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
                request, stream=False, **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                error = self._deserialize.failsafe_deserialize(_models.ErrorResponseAutoGenerated, pipeline_response)
                raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

            return pipeline_response

        return AsyncItemPaged(get_next, extract_data)

    get_all.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.AlertsManagement/alerts"}  # type: ignore

    @distributed_trace_async
    async def get_by_id(self, alert_id: str, **kwargs: Any) -> _models.Alert:
        """Get a specific alert.

        Get information related to a specific alert.

        :param alert_id: Unique ID of an alert instance. Required.
        :type alert_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Alert or the result of cls(response)
        :rtype: ~azure.mgmt.alertsmanagement.models.Alert
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.Alert]

        request = build_get_by_id_request(
            alert_id=alert_id,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get_by_id.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponseAutoGenerated, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("Alert", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_by_id.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.AlertsManagement/alerts/{alertId}"}  # type: ignore

    @distributed_trace_async
    async def change_state(
        self, alert_id: str, new_state: Union[str, "_models.AlertState"], comment: Optional[str] = None, **kwargs: Any
    ) -> _models.Alert:
        """Change the state of an alert.

        :param alert_id: Unique ID of an alert instance. Required.
        :type alert_id: str
        :param new_state: New state of the alert. Known values are: "New", "Acknowledged", and
         "Closed". Required.
        :type new_state: str or ~azure.mgmt.alertsmanagement.models.AlertState
        :param comment: reason of change alert state. Default value is None.
        :type comment: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: Alert or the result of cls(response)
        :rtype: ~azure.mgmt.alertsmanagement.models.Alert
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        content_type = kwargs.pop("content_type", _headers.pop("Content-Type", "application/json"))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.Alert]

        if comment is not None:
            _content = self._serialize.body(comment, "str")
        else:
            _content = None

        request = build_change_state_request(
            alert_id=alert_id,
            subscription_id=self._config.subscription_id,
            new_state=new_state,
            api_version=api_version,
            content_type=content_type,
            content=_content,
            template_url=self.change_state.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponseAutoGenerated, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("Alert", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    change_state.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.AlertsManagement/alerts/{alertId}/changestate"}  # type: ignore

    @distributed_trace_async
    async def get_history(self, alert_id: str, **kwargs: Any) -> _models.AlertModification:
        """Get the history of an alert, which captures any monitor condition changes (Fired/Resolved) and
        alert state changes (New/Acknowledged/Closed).

        :param alert_id: Unique ID of an alert instance. Required.
        :type alert_id: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: AlertModification or the result of cls(response)
        :rtype: ~azure.mgmt.alertsmanagement.models.AlertModification
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.AlertModification]

        request = build_get_history_request(
            alert_id=alert_id,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get_history.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponseAutoGenerated, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("AlertModification", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_history.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.AlertsManagement/alerts/{alertId}/history"}  # type: ignore

    @distributed_trace_async
    async def get_summary(
        self,
        groupby: Union[str, "_models.AlertsSummaryGroupByFields"],
        include_smart_groups_count: Optional[bool] = None,
        target_resource: Optional[str] = None,
        target_resource_type: Optional[str] = None,
        target_resource_group: Optional[str] = None,
        monitor_service: Optional[Union[str, "_models.MonitorService"]] = None,
        monitor_condition: Optional[Union[str, "_models.MonitorCondition"]] = None,
        severity: Optional[Union[str, "_models.Severity"]] = None,
        alert_state: Optional[Union[str, "_models.AlertState"]] = None,
        alert_rule: Optional[str] = None,
        time_range: Optional[Union[str, "_models.TimeRange"]] = None,
        custom_time_range: Optional[str] = None,
        **kwargs: Any
    ) -> _models.AlertsSummary:
        """Get a summarized count of your alerts grouped by various parameters (e.g. grouping by
        'Severity' returns the count of alerts for each severity).

        :param groupby: This parameter allows the result set to be grouped by input fields (Maximum 2
         comma separated fields supported). For example, groupby=severity or
         groupby=severity,alertstate. Known values are: "severity", "alertState", "monitorCondition",
         "monitorService", "signalType", and "alertRule". Required.
        :type groupby: str or ~azure.mgmt.alertsmanagement.models.AlertsSummaryGroupByFields
        :param include_smart_groups_count: Include count of the SmartGroups as part of the summary.
         Default value is 'false'. Default value is None.
        :type include_smart_groups_count: bool
        :param target_resource: Filter by target resource( which is full ARM ID) Default value is
         select all. Default value is None.
        :type target_resource: str
        :param target_resource_type: Filter by target resource type. Default value is select all.
         Default value is None.
        :type target_resource_type: str
        :param target_resource_group: Filter by target resource group name. Default value is select
         all. Default value is None.
        :type target_resource_group: str
        :param monitor_service: Filter by monitor service which generates the alert instance. Default
         value is select all. Known values are: "Application Insights", "ActivityLog Administrative",
         "ActivityLog Security", "ActivityLog Recommendation", "ActivityLog Policy", "ActivityLog
         Autoscale", "Log Analytics", "Nagios", "Platform", "SCOM", "ServiceHealth", "SmartDetector",
         "VM Insights", and "Zabbix". Default value is None.
        :type monitor_service: str or ~azure.mgmt.alertsmanagement.models.MonitorService
        :param monitor_condition: Filter by monitor condition which is either 'Fired' or 'Resolved'.
         Default value is to select all. Known values are: "Fired" and "Resolved". Default value is
         None.
        :type monitor_condition: str or ~azure.mgmt.alertsmanagement.models.MonitorCondition
        :param severity: Filter by severity.  Default value is select all. Known values are: "Sev0",
         "Sev1", "Sev2", "Sev3", and "Sev4". Default value is None.
        :type severity: str or ~azure.mgmt.alertsmanagement.models.Severity
        :param alert_state: Filter by state of the alert instance. Default value is to select all.
         Known values are: "New", "Acknowledged", and "Closed". Default value is None.
        :type alert_state: str or ~azure.mgmt.alertsmanagement.models.AlertState
        :param alert_rule: Filter by specific alert rule.  Default value is to select all. Default
         value is None.
        :type alert_rule: str
        :param time_range: Filter by time range by below listed values. Default value is 1 day. Known
         values are: "1h", "1d", "7d", and "30d". Default value is None.
        :type time_range: str or ~azure.mgmt.alertsmanagement.models.TimeRange
        :param custom_time_range: Filter by custom time range in the format
         :code:`<start-time>`/:code:`<end-time>`  where time is in (ISO-8601 format)'. Permissible
         values is within 30 days from  query time. Either timeRange or customTimeRange could be used
         but not both. Default is none. Default value is None.
        :type custom_time_range: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: AlertsSummary or the result of cls(response)
        :rtype: ~azure.mgmt.alertsmanagement.models.AlertsSummary
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop("api_version", _params.pop("api-version", self._config.api_version))  # type: str
        cls = kwargs.pop("cls", None)  # type: ClsType[_models.AlertsSummary]

        request = build_get_summary_request(
            subscription_id=self._config.subscription_id,
            groupby=groupby,
            include_smart_groups_count=include_smart_groups_count,
            target_resource=target_resource,
            target_resource_type=target_resource_type,
            target_resource_group=target_resource_group,
            monitor_service=monitor_service,
            monitor_condition=monitor_condition,
            severity=severity,
            alert_state=alert_state,
            alert_rule=alert_rule,
            time_range=time_range,
            custom_time_range=custom_time_range,
            api_version=api_version,
            template_url=self.get_summary.metadata["url"],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request, stream=False, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            error = self._deserialize.failsafe_deserialize(_models.ErrorResponseAutoGenerated, pipeline_response)
            raise HttpResponseError(response=response, model=error, error_format=ARMErrorFormat)

        deserialized = self._deserialize("AlertsSummary", pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get_summary.metadata = {"url": "/subscriptions/{subscriptionId}/providers/Microsoft.AlertsManagement/alertsSummary"}  # type: ignore
