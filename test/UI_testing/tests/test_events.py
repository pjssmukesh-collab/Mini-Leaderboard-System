import pytest
import time
from pages.creator_dashboard_page import CreatorDashboardPage
from pages.create_event_page import CreateEventPage

@pytest.mark.ui
@pytest.mark.events
class TestEvents:
    """Test suite for tournament event creation, form validation, and dashboard management."""

    def test_create_event_page_loads_correctly(self, authenticated_creator):
        """Verify that the tournament creation page loads with all form controls."""
        create_page = CreateEventPage(authenticated_creator)
        create_page.open_create_event()
        
        assert create_page.is_page_loaded(), "Create event form failed to load."
        assert create_page.is_visible(create_page.NAME_INPUT), "Name input missing."
        assert create_page.is_visible(create_page.EVENT_TYPE_INPUT), "Category input missing."
        assert create_page.is_visible(create_page.SUBMIT_BUTTON), "Submit button missing."

    def test_create_event_required_validation(self, authenticated_creator):
        """Verify HTML5 validation triggers when submitting empty tournament form."""
        create_page = CreateEventPage(authenticated_creator)
        create_page.open_create_event()
        create_page.submit_form()
        
        name_val = create_page.get_name_validation_message()
        assert len(name_val) > 0, "Expected required validation on tournament name."

    def test_create_event_cancel_navigates_to_dashboard(self, authenticated_creator):
        """Verify clicking cancel returns to creator dashboard."""
        create_page = CreateEventPage(authenticated_creator)
        create_page.open_create_event()
        create_page.click_cancel()
        
        dashboard = CreatorDashboardPage(authenticated_creator)
        assert dashboard.wait_for_url_contains("/creator/dashboard"), "Cancel did not return to dashboard."

    def test_successful_event_creation_flow(self, authenticated_creator):
        """Verify complete tournament creation with preset category and participant limit."""
        create_page = CreateEventPage(authenticated_creator)
        create_page.open_create_event()
        
        event_name = f"Championship_{int(time.time())}"
        create_page.select_preset_category("Gaming")
        create_page.fill_form(
            name=event_name,
            event_type="gaming",
            description="End-to-End automated testing tournament",
            participant_limit="32"
        )
        create_page.submit_form()
        
        # On success, CreateEvent.jsx navigates to /creator/events/:id/rules
        assert create_page.wait_for_url_contains("/rules", timeout=8), (
            f"Event creation did not advance to Rule Builder! Current URL: {create_page.get_current_url()}"
        )
