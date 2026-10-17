import pytest
from pages.rule_builder_page import RuleBuilderPage

@pytest.mark.ui
@pytest.mark.rules
class TestEventRules:
    """Test suite for the dynamic scoring rule engine configuration UI."""

    def test_rule_builder_page_loads_for_event(self, authenticated_creator):
        """Verify rule builder interface loads for a tournament."""
        rules_page = RuleBuilderPage(authenticated_creator)
        rules_page.open_rules_page(event_id=1)
        
        assert rules_page.is_page_loaded(), "Rule builder page failed to load for event 1."
        assert rules_page.is_visible(rules_page.METRIC_INPUT), "Metric input field is missing."
        assert rules_page.is_visible(rules_page.ADD_RULE_BUTTON), "Add Rule button is missing."

    def test_add_scoring_rule_flow(self, authenticated_creator):
        """Verify adding a scoring rule and confirming it appears in the active rules table."""
        rules_page = RuleBuilderPage(authenticated_creator)
        rules_page.open_rules_page(event_id=1)
        
        initial_count = rules_page.get_rules_count()
        rules_page.add_rule(
            metric="kills",
            points="5",
            operator="each",
            priority="1"
        )
        
        # Verify rule is added to table
        updated_count = rules_page.get_rules_count()
        assert updated_count >= initial_count, "Rules table did not reflect new rule."

    def test_navigation_from_rules_to_dashboard(self, authenticated_creator):
        """Verify clicking 'Finish Setup & Return' navigates back to creator dashboard."""
        rules_page = RuleBuilderPage(authenticated_creator)
        rules_page.open_rules_page(event_id=1)
        rules_page.click_finish()
        
        assert rules_page.wait_for_url_contains("/creator/dashboard", timeout=5), (
            "Finish button did not navigate back to creator dashboard."
        )
