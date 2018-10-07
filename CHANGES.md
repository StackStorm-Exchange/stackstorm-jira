# Change Log

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
