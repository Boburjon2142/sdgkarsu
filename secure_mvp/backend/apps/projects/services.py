from apps.common.audit import record_audit_event


def create_project(request, serializer):
    project = serializer.save()
    record_audit_event(request, "project.created", target=project)
    return project


def update_project(request, serializer):
    project = serializer.save()
    record_audit_event(request, "project.updated", target=project)
    return project


def delete_project(request, project):
    record_audit_event(request, "project.deleted", target=project)
    project.delete()


def create_project_document(request, serializer):
    document = serializer.save()
    record_audit_event(
        request,
        "project.document_uploaded",
        target=document,
        metadata={"project_id": document.project_id},
    )
    return document
