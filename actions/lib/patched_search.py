from __future__ import annotations

import json
import warnings
from typing import Any, Generic, Iterable, overload

from jira import JIRA
from jira.client import ResourceType, cloud_api
from jira.resources import Issue

JIRA_BASE_URL = JIRA.JIRA_BASE_URL


class ResultList(list, Generic[ResourceType]):
    def __init__(
        self,
        iterable: Iterable | None = None,
        _startAt: int = 0,
        _maxResults: int = 0,
        _total: int | None = None,
        _isLast: bool | None = None,
        _nextPageToken: str | None = None,
    ) -> None:
        """Results List.

        Args:
            iterable (Iterable): [description]. Defaults to None.
            _startAt (int): Start page. Defaults to 0.
            _maxResults (int): Max results per page. Defaults to 0.
            _total (Optional[int]): Total results from query. Defaults to 0.
            _isLast (Optional[bool]): True to mark this page is the last page? (Default: ``None``).
            _nextPageToken (Optional[str]): Token for fetching the next page of results. Defaults to None.
             see `The official API docs <https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#expansion:~:text=for%20all%20operations.-,isLast,-indicates%20whether%20the>`_
        """
        if iterable is not None:
            list.__init__(self, iterable)
        else:
            list.__init__(self)

        self.startAt = _startAt
        self.maxResults = _maxResults
        # Optional parameters:
        self.isLast = _isLast
        self.total = _total if _total is not None else len(self)

        self.iterable: list[ResourceType] = list(iterable) if iterable else []
        self.current = self.startAt
        self.nextPageToken = _nextPageToken

    def __next__(self) -> ResourceType:  # type:ignore[misc]
        self.current += 1
        if self.current > self.total:
            raise StopIteration
        else:
            return self.iterable[self.current - 1]

    def __iter__(self) -> Iterator[ResourceType]:
        return super().__iter__()

    # fmt: off
    # The mypy error we ignore is about returning a contravariant type.
    # As this class is a List of a generic 'Resource' class
    # this is the right way to specify that the output is the same as which
    # the class was initialized with.
    @overload
    def __getitem__(self, i: SupportsIndex) -> ResourceType: ...  # type:ignore[misc]  # noqa: E704
    @overload
    def __getitem__(self, s: slice) -> list[ResourceType]: ...  # type:ignore[misc]  # noqa: E704
    def __getitem__(self, slice_or_index): # noqa: E301,E261
        return list.__getitem__(self, slice_or_index)
    # fmt: on


def patched_search_issues(
    self,
    jql_str: str,
    startAt: int = 0,
    maxResults: int = 50,
    validate_query: bool = True,
    fields: str | list[str] | None = "*all",
    expand: str | None = None,
    properties: str | None = None,
    *,
    json_result: bool = False,
    use_post: bool = False,
) -> dict[str, Any] | ResultList[Issue]:
    """Get a :class:`~jira.client.ResultList` of issue Resources matching a JQL search string.

    Args:
        jql_str (str): The JQL search string.
        startAt (int): Index of the first issue to return. (Default: ``0``)
        maxResults (int): Maximum number of issues to return.
            Total number of results is available in the ``total`` attribute of the returned :class:`ResultList`.
            If maxResults evaluates to False, it will try to get all issues in batches. (Default: ``50``)
        validate_query (bool): True to validate the query. (Default: ``True``)
        fields (Optional[Union[str, List[str]]]): comma-separated string or list of issue fields to include in the results.
            Default is to include all fields.
        expand (Optional[str]): extra information to fetch inside each resource
        properties (Optional[str]): extra properties to fetch inside each result
        json_result (bool): True to return a JSON response. When set to False a :class:`ResultList` will be returned. (Default: ``False``)
        use_post (bool): True to use POST endpoint to fetch issues.

    Returns:
        Union[Dict,ResultList]: Dict if ``json_result=True``
    """
    if isinstance(fields, str):
        fields = fields.split(",")
    elif fields is None:
        fields = ["*all"]

    if self._is_cloud:
        if startAt == 0:
            return self.enhanced_search_issues(
                jql_str=jql_str,
                maxResults=maxResults,
                fields=fields,
                expand=expand,
                properties=properties,
                json_result=json_result,
                use_post=use_post,
            )
        else:
            raise JIRAError(
                "The `search` API is deprecated in Jira Cloud. Use `enhanced_search_issues` method instead."
            )

    # this will translate JQL field names to REST API Name
    # most people do know the JQL names so this will help them use the API easier
    untranslate = {}  # use to add friendly aliases when we get the results back
    if self._fields_cache:
        for i, field in enumerate(fields):
            if field in self._fields_cache:
                untranslate[self._fields_cache[field]] = fields[i]
                fields[i] = self._fields_cache[field]

    search_params = {
        "jql": jql_str,
        "startAt": startAt,
        "validateQuery": validate_query,
        "fields": fields,
        "expand": expand,
        "properties": properties,
    }
    # for the POST version of this endpoint Jira
    # complains about unrecognized field "properties"
    if use_post:
        search_params.pop("properties")
    if json_result:
        search_params["maxResults"] = maxResults
        if not maxResults:
            warnings.warn(
                "All issues cannot be fetched at once, when json_result parameter is set",
                Warning,
            )
        r_json: dict[str, Any] = self._get_json(
            "search", params=search_params, use_post=use_post
        )
        return r_json

    issues = self._fetch_pages(
        Issue,
        "issues",
        "search",
        startAt,
        maxResults,
        search_params,
        use_post=use_post,
    )

    if untranslate:
        iss: Issue
        for iss in issues:
            for k, v in untranslate.items():
                if iss.raw:
                    if k in iss.raw.get("fields", {}):
                        iss.raw["fields"][v] = iss.raw["fields"][k]

    return issues


@cloud_api
def enhanced_search_issues(
    self,
    jql_str: str,
    nextPageToken: str | None = None,
    maxResults: int = 50,
    fields: str | list[str] | None = "*all",
    expand: str | None = None,
    reconcileIssues: list[int] | None = None,
    properties: str | None = None,
    *,
    json_result: bool = False,
    use_post: bool = False,
) -> dict[str, Any] | ResultList[Issue]:
    """Get a :class:`~jira.client.ResultList` of issue Resources matching a JQL search string.

    Args:
        jql_str (str): The JQL search string.
        nextPageToken (Optional[str]): Token for paginated results.
        maxResults (int): Maximum number of issues to return.
            Total number of results is available in the ``total`` attribute of the returned :class:`ResultList`.
            If maxResults evaluates to False, it will try to get all issues in batches. (Default: ``50``)
        fields (Optional[Union[str, List[str]]]): comma-separated string or list of issue fields to include in the results.
            Default is to include all fields If you don't require fields, set it to empty string ``''``.
        expand (Optional[str]): extra information to fetch inside each resource.
        reconcileIssues (Optional[List[int]]): List of issue IDs to reconcile.
        properties (Optional[str]): extra properties to fetch inside each result
        json_result (bool): True to return a JSON response. When set to False a :class:`ResultList` will be returned. (Default: ``False``)
        use_post (bool): True to use POST endpoint to fetch issues.

    Returns:
        Union[Dict, ResultList]: JSON Dict if ``json_result=True``, otherwise a `ResultList`.
    """
    if isinstance(fields, str):
        fields = fields.split(",")
    elif fields is None:
        fields = ["*all"]

    untranslate = {}  # use to add friendly aliases when we get the results back
    if fields:
        # this will translate JQL field names to REST API Name
        # most people do know the JQL names so this will help them use the API easier
        if self._fields_cache:
            for i, field in enumerate(fields):
                if field in self._fields_cache:
                    untranslate[self._fields_cache[field]] = fields[i]
                    fields[i] = self._fields_cache[field]

    search_params: dict[str, Any] = {
        "jql": jql_str,
        "fields": fields,
        "expand": expand,
        "properties": properties,
        "reconcileIssues": reconcileIssues or [],
    }
    if nextPageToken:
        search_params["nextPageToken"] = nextPageToken

    if json_result:
        if not maxResults:
            warnings.warn(
                "All issues cannot be fetched at once, when json_result parameter is set",
                Warning,
            )
        else:
            search_params["maxResults"] = maxResults
        r_json: dict[str, Any] = self._get_json(
            "search/jql", params=search_params, use_post=use_post
        )
        return r_json

    issues = self._fetch_pages_searchToken(
        item_type=Issue,
        items_key="issues",
        request_path="search/jql",
        maxResults=maxResults,
        params=search_params,
        use_post=use_post,
    )

    if untranslate:
        iss: Issue
        for iss in issues:
            for k, v in untranslate.items():
                if iss.raw:
                    if k in iss.raw.get("fields", {}):
                        iss.raw["fields"][v] = iss.raw["fields"][k]

    return issues


@cloud_api
def _fetch_pages_searchToken(
    self,
    item_type: type[ResourceType],
    items_key: str | None,
    request_path: str,
    maxResults: int = 50,
    params: dict[str, Any] | None = None,
    base: str = JIRA_BASE_URL,
    use_post: bool = False,
) -> ResultList[ResourceType]:
    """Fetch from a paginated API endpoint using `nextPageToken`.

    Args:
        item_type (Type[Resource]): Type of single item. Returns a `ResultList` of such items.
        items_key (Optional[str]): Path to the items in JSON returned from the server.
        request_path (str): Path in the request URL.
        maxResults (int): Maximum number of items to return per page. (Default: 50)
        params (Dict[str, Any]): Parameters to be sent with the request.
        base (str): Base URL for the requests.
        use_post (bool): Whether to use POST instead of GET.

    Returns:
        ResultList: List of fetched items.
    """
    DEFAULT_BATCH = 100  # Max batch size per request
    fetch_all = maxResults in (0, False)  # If False/0, fetch everything

    page_params = (params or {}).copy()  # Ensure params isn't modified
    page_params["maxResults"] = DEFAULT_BATCH if fetch_all else maxResults

    # Use caller-provided nextPageToken if present
    nextPageToken: str | None = page_params.get("nextPageToken")
    items: list[ResourceType] = []

    while True:
        # Ensure nextPageToken is set in params if it exists
        if nextPageToken:
            page_params["nextPageToken"] = nextPageToken
        else:
            page_params.pop("nextPageToken", None)

        response = self._get_json(
            request_path, params=page_params, base=base, use_post=use_post
        )
        items.extend(self._get_items_from_page(item_type, items_key, response))
        nextPageToken = response.get("nextPageToken")
        if not fetch_all or not nextPageToken:
            break

    return ResultList(items, _nextPageToken=nextPageToken)


def _get_items_from_page(
    self,
    item_type: type[ResourceType],
    items_key: str | None,
    resource: dict[str, Any],
) -> list[ResourceType]:
    try:
        return [
            # We need to ignore the type here, as 'Resource' is an option
            item_type(self._options, self._session, raw_issue_json)  # type: ignore
            for raw_issue_json in (resource[items_key] if items_key else resource)
        ]
    except KeyError as e:
        # improving the error text so we know why it happened
        raise KeyError(str(e) + " : " + json.dumps(resource))


JIRA._fetch_pages_searchToken = _fetch_pages_searchToken
JIRA._get_items_from_page = _get_items_from_page
JIRA.enhanced_search_issues = enhanced_search_issues
JIRA.search_issues = patched_search_issues
