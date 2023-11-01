__all__ = [
    'to_issue_dict',
    'to_comment_dict'
]


def to_issue_dict(issue, include_comments=False, include_attachments=False,
                  include_customfields=False, include_components=False, include_subtasks=False,
                  include_links=False):
    """
    :rtype: ``dict``
    """
    split = issue.permalink().split(' - ', 1)
    url = split[0]

    if issue.fields.resolution:
        resolution = issue.fields.resolution.name
    else:
        resolution = None

    if issue.fields.reporter:
        reporter = issue.fields.reporter.displayName
    else:
        reporter = None

    if issue.fields.assignee:
        assignee = issue.fields.assignee.displayName
    else:
        assignee = None

    result = {
        'id': issue.id,
        'key': issue.key,
        'url': url,
        'summary': issue.fields.summary,
        'description': issue.fields.description,
        'status': issue.fields.status.name,
        'priority': issue.fields.priority.name if hasattr(issue.fields, 'priority') else None,
        'resolution': resolution,
        'labels': issue.fields.labels if hasattr(issue.fields, 'labels') else [],
        'reporter': reporter,
        'assignee': assignee,
        'created_at': issue.fields.created,
        'updated_at': issue.fields.updated,
        'resolved_at': issue.fields.resolutiondate
    }

    if include_customfields:
        for key in issue.raw['fields']:
            if not key.startswith('customfield_'):
                continue

            result[key] = issue.raw['fields'][key]

    if include_comments:
        result['comments'] = []

        for comment in issue.fields.comment.comments:
            item = to_comment_dict(comment)
            result['comments'].append(item)

    if include_attachments:
        result['attachments'] = []

        for attachment in issue.fields.attachment:
            item = to_attachment_dict(attachment)
            result['attachments'].append(item)

    if include_components:
        result['components'] = [to_component_dict(c) for c in issue.fields.components]

    if include_subtasks:
        result['subtasks'] = [to_subtask_dict(s) for s in issue.fields.subtasks]
    
    if include_links:
        result['links'] = [to_links_dict(i) for i in issue.fields.issuelinks]

    return result


def to_comment_dict(comment):
    """
    :rtype: ``dict``
    """
    result = {
        'id': comment.id,
        'body': comment.body
    }
    return result


def to_component_dict(component):
    """
    :rtype: ``dict``
    """
    result = {
        'id': component.id,
        'name': component.name
    }
    return result


def to_subtask_dict(subtask):
    """
    :rtype: ``dict``
    """
    result = {
        'id': subtask.id,
        'key': subtask.key,
        'summary': subtask.fields.summary
    }
    return result


def to_attachment_dict(attachment):
    """
    :rtype: ``dict``
    """
    result = {
        'filename': attachment.filename,
        'size': attachment.size,
        'created_at': attachment.created,
        'content': attachment.content,
    }
    return result

def to_links_dict(issue):
    """
    :rtype: ``dict``
    """
    result = {
        'id': issue.raw.get('id'),
        'key': issue.raw.get('outwardIssue', issue.raw.get('inwardIssue')).get('key'),
        'summary': issue.raw.get('outwardIssue', issue.raw.get('inwardIssue'))
        .get('fields').get('summary'),
        'status': issue.raw.get('outwardIssue', issue.raw.get('inwardIssue')).get('fields')
        .get('status').get('name'),
        'type': issue.raw.get('type').get('outward') if issue.raw.get('outwardIssue')
        else issue.raw.get('type').get('inward'),
    }
    return result

def fmt_field_value(field, value):
    """
    Returns specific field values in formats required by JIRA
    """
    if field == "priority":
        value = {"name": value}
    if field == "labels":
        value = value.split()
    return value
