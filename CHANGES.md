# Change Log

## 1.1.0

- Add PAT-based authentication (PR #47)

## 1.0.0

* Drop Python 2.7 support

## 0.16.0

- Add new ``jira.get_issue_components`` action
- Add new ``jira.get_issue_subtasks`` action

## 0.15.0

- Add new action `link_issue`.  This allows linking issues together

## 0.14.0

- Support cookie-based authentication (PR #42)

## 0.13.1

- Remove cryptography, pyjwt, pyyaml requirements since we don't use them (PR #41)

## 0.13.0

- Add ``validate`` option to pack config to enable validating credentials
  before running any actions (PR #33)
  Special thanks to @guymatz for this contribution

## 0.12.1

- Minor linting change

## 0.12.0

- Add new ``jira.add_field_value`` action

## 0.11.0

- Add new ``jira.transition_issue_by_name`` action

## 0.10.1

- Updated PyYAML to 4.2b4 for CVE-2017-18342

## 0.10.0

- Add new ``jira.assign_issues`` action

## 0.9.0

- Add new ``jira.issues_tracker_for_apiv2`` sensor

## 0.8.1

- Version bump to fix tagging issue, no code changes

## 0.8.0

- Adding support for BASIC authentication

## 0.7.1

- Return custom fields in formatter

## 0.7.0

- Add new ``jira.search_issues`` action

## 0.6.0

- Add new ``jira.get_issue_comments`` action
- Add new ``jira.get_issue_attachments`` action
- Add new ``include_comments`` and ``include_attachments`` parameter to
  ``jira.get_issue`` action which allows users to retrieve comments and
  attachments in a single call when retrieving issue details. For backward
  compatibility reasons, both arguments default to ``False``.

## 0.5.1

- Added 'verify' option to disable SSL certificate verification

## 0.5.0

- Updated action `runner_type` from `run-python` to `python-script`

## 0.4.0

- Rename `config.yaml` to `config.schema.yaml` and update to use schema.
