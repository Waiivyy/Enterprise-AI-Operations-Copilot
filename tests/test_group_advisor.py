from app.models.user import UserProfile
from app.tools.group_advisor import recommend_groups


def test_group_advisor_recommends_department_region_and_employee_groups():
    user = UserProfile(
        display_name="Sara Holm",
        email="sara.holm@example.invalid",
        department="Engineering",
        region="Europe",
        employment_type="full-time",
    )

    groups = recommend_groups(user)
    group_ids = {group.group_id for group in groups}

    assert {"group-engineering", "group-europe", "group-employees"} <= group_ids
