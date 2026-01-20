# Change Log

## 3.2.3
- Addresses [#87](https://github.com/StackStorm-Exchange/stackstorm-jira/issues/87) JIRA sensor failure due to [deprecation of /v2/search endpoint](https://developer.atlassian.com/changelog/#CHANGE-2046)

## 3.2.2
- Addresses [#87](https://github.com/StackStorm-Exchange/stackstorm-jira/issues/87) search failure due to [deprecation of /v2/search endpoint](https://developer.atlassian.com/changelog/#CHANGE-2046)

## 3.2.1
- Fixed the deafult attribute invocation for jira field ``description`` to verify that the attribute exists first. If ``description`` attribute does not exist then return ``null``.

## 3.2.0
- Add new feature to ``jira.get_issue`` to allow for stripping of Jinja templating artifacts from resulting output. (Removes instances of {{ }} from results.)

  Example: You pull a jira with ``code`` block in a comment or the description. To the API that shows up as {{ code }} which is jinja Templating and will cause
  issues when trying to use that output anywhere else in a workflow as it cannot find the `code` variable in the context.


## 3.0.1

- Fixed bug with `update_dashboard` action sending the wrong payload.

## 3.0.0

- Drop support for `python 3.6`
- Add new ``jira.add_gadget`` action
- Add new ``jira.copy_dashboard`` action
- Add new ``jira.create_dashboard`` action
- Add new ``jira.delete_dashboard_item_property`` action
- Add new ``jira.delete_dashboard`` action
- Add new ``jira.get_available_gadgets`` action
- Add new ``jira.get_dashboard_gadgets`` action
- Add new ``jira.get_dashboard_item_property_keys`` action
- Add new ``jira.get_dashboard_item_property`` action
- Add new ``jira.remove_gadget`` actionn
- Add new ``jira.set_dashboard_item_property`` action
- Add new ``jira.update_dashboard_automatic_refresh`` action
- Add new ``jira.update_dashboard_item_property`` action
- Add new ``jira.update_dashboard`` action
- Add new ``jira.update_gadget`` action

## 2.6.0

- Add new ``jira.get_issue_links`` action

- Evaluate if an issue has a priority set before attempting to get the priority

## 2.5.1

- Improve handling of `priority` field in update_field_value action to address [#65]

## 2.5.0

- Added multithreading in linking multiple issue functionality to speed up the response.

## 2.4.2

- Update `formatters.py` to include `priority` field

## 2.4.1

- Update `search_issue` to include `include_components` and `include_subtasks` as flags

## 2.4.0

- `add_field_value` and `update_field_value` actions now return a dictionary representation of the issue being modified. Previously these actions would return
only the `labels` field if it exists as an attribute. This addresses [#53](https://github.com/StackStorm-Exchange/stackstorm-jira/issues/53) but is also beneficial for displaying other field values (inclusive of `labels`) that may have been updated.

- Fix for [#54](https://github.com/StackStorm-Exchange/stackstorm-jira/issues/54) which prevents callers of the `update_field_value` action from updating `labels` which must be passed as a list via the api. As labels cannot contain spaces we split
the `value` field of this action on whitespace in the case where `field` == `"labels"`. Example invocation:

```
st2 action execute jira.update_field_value issue_key=NETOPS-1 field=labels value='Label1 Label2'
```

## 2.3.1

- Update `README.md` to include `api_token` as an auth method

## 2.3.0

- Add new `api_token` auth method.  This authentication method is different than a `pat` authentication request. (PR #54)
- Added `pat` and `cookie` auth methods to the sensors.

## 2.2.0

- Adjust jql in sensor to better support large JIRA projects
- Detect new issues by id vs comparing to an in-memory list

## 2.1.0

- Add new ``jira.bulk_link_issues`` action (PR #50)

## 2.0.0

- [#48](https://github.com/StackStorm-Exchange/stackstorm-jira/issues/48) Update `jira==3.2.0`

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
