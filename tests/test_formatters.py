from functools import partial
from types import SimpleNamespace

from lib.formatters import to_issue_dict, to_links_dict


def test_to_issue_dict_includes_metadata() -> None:
    fields = SimpleNamespace(
        assignee=SimpleNamespace(displayName="Assignee"),
        created="2026-07-29T10:00:00.000+0000",
        description="Description",
        issuetype=SimpleNamespace(name="Task"),
        labels=["example"],
        priority=SimpleNamespace(name="High"),
        reporter=SimpleNamespace(displayName="Reporter"),
        resolution=SimpleNamespace(name="Done"),
        resolutiondate="2026-07-30T10:00:00.000+0000",
        status=SimpleNamespace(
            name="Completed",
            statusCategory=SimpleNamespace(name="Done"),
        ),
        summary="Example issue",
        updated="2026-07-30T10:00:00.000+0000",
    )
    issue = SimpleNamespace(
        fields=fields,
        id="10001",
        key="TEST-1",
        permalink=partial(str, "https://jira.example.com/browse/TEST-1 - Example issue"),
    )

    assert to_issue_dict(issue) == {
        "id": "10001",
        "key": "TEST-1",
        "url": "https://jira.example.com/browse/TEST-1",
        "summary": "Example issue",
        "description": "Description",
        "status": "Completed",
        "issue_type": "Task",
        "status_category": "Done",
        "priority": "High",
        "resolution": "Done",
        "labels": ["example"],
        "reporter": "Reporter",
        "assignee": "Assignee",
        "created_at": "2026-07-29T10:00:00.000+0000",
        "updated_at": "2026-07-30T10:00:00.000+0000",
        "resolved_at": "2026-07-30T10:00:00.000+0000",
    }


def test_to_issue_dict_handles_missing_optional_metadata() -> None:
    fields = SimpleNamespace(
        assignee=None,
        created="2026-07-29T10:00:00.000+0000",
        description=None,
        labels=[],
        reporter=None,
        resolution=None,
        resolutiondate=None,
        status=SimpleNamespace(name="Open"),
        summary="Partial issue",
        updated="2026-07-30T10:00:00.000+0000",
    )
    issue = SimpleNamespace(
        fields=fields,
        id="10002",
        key="TEST-2",
        permalink=partial(str, "https://jira.example.com/browse/TEST-2 - Partial issue"),
    )

    result = to_issue_dict(issue)

    assert result["issue_type"] is None
    assert result["status_category"] is None


def test_to_links_dict_includes_outward_issue_type() -> None:
    link = SimpleNamespace(
        raw={
            "id": "20001",
            "outwardIssue": {
                "key": "TEST-3",
                "fields": {
                    "issuetype": {"name": "Task"},
                    "status": {"name": "To Do"},
                    "summary": "Linked issue",
                },
            },
            "type": {"inward": "is caused by", "outward": "causes"},
        }
    )

    assert to_links_dict(link) == {
        "id": "20001",
        "key": "TEST-3",
        "summary": "Linked issue",
        "status": "To Do",
        "type": "causes",
        "issue_type": "Task",
    }


def test_to_links_dict_includes_inward_issue_type() -> None:
    link = SimpleNamespace(
        raw={
            "id": "20002",
            "inwardIssue": {
                "key": "TEST-4",
                "fields": {
                    "issuetype": {"name": "Bug"},
                    "status": {"name": "Done"},
                    "summary": "Related issue",
                },
            },
            "type": {"inward": "is caused by", "outward": "causes"},
        }
    )

    assert to_links_dict(link) == {
        "id": "20002",
        "key": "TEST-4",
        "summary": "Related issue",
        "status": "Done",
        "type": "is caused by",
        "issue_type": "Bug",
    }


def test_to_links_dict_handles_missing_optional_fields() -> None:
    link = SimpleNamespace(
        raw={
            "id": "20003",
            "outwardIssue": {"key": "TEST-5", "fields": {}},
            "type": {"outward": "relates to"},
        }
    )

    assert to_links_dict(link) == {
        "id": "20003",
        "key": "TEST-5",
        "summary": None,
        "status": None,
        "type": "relates to",
        "issue_type": None,
    }
