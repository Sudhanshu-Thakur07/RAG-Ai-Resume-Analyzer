from services.qdrant_service import search, extract_context


def get_interview_questions(role, top_k=10):

    query = f"""
    Interview questions for the role of {role}.

    Find interview questions specifically related to this role.
    Include technical, practical and role-specific questions.
    """

    points = search(
        query,
        top_k=top_k
    )

    context = extract_context(points)

    return context