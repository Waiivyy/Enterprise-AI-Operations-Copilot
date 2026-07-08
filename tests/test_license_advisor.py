from app.models.user import UserProfile
from app.tools.license_advisor import recommend_license


def test_engineering_employee_in_europe_gets_business_premium():
    user = UserProfile(
        display_name="Sara Holm",
        email="sara.holm@example.invalid",
        department="Engineering",
        region="Europe",
        employment_type="full-time",
    )

    recommendation = recommend_license(user)

    assert recommendation.sku_id == "sku-m365-business-premium"
    assert recommendation.name == "Microsoft 365 Business Premium"
    assert "Engineering collaboration baseline" in recommendation.reason
