from __future__ import annotations

from lib.base import BaseJiraAction

__all__ = ["SearchJiraUsersAction"]


class SearchJiraUsersAction(BaseJiraAction):
    def run(
        self,
        query,
        start_at: int = 0,
        max_results: int = 50,
        include_active: bool = True,
        include_inactive: bool = False,
    ) -> dict[str, str]:
        users = self._client.search_users(
            query=query,
            startAt=start_at,
            maxResults=max_results,
            includeActive=include_active,
            includeInactive=include_inactive,
        )
        results = []

        for user in users:
            results.append(user.raw)

        return results
