from app.tools.graph_mock import troubleshoot_access


def test_access_troubleshooting_detects_missing_teams_license():
    finding = troubleshoot_access("maria.novak@example.invalid", "Teams")

    assert finding.likely_cause == "Teams license missing"
    assert any("sku-m365-business-basic" in item for item in finding.evidence)
    assert finding.confidence >= 0.8


def test_access_troubleshooting_detects_missing_group_membership():
    finding = troubleshoot_access("lena.ortiz@example.invalid", "Teams")

    assert finding.likely_cause == "Teams group membership missing"
    assert any("group-employees" in item for item in finding.evidence)
    assert "Review group membership and app assignment policy." in finding.recommended_actions
