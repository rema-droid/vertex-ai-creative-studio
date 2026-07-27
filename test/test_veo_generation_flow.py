import pytest
from unittest.mock import patch, MagicMock
import os
import sys

# Setup sys.path to allow imports from the parent directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.veo import on_click_veo
from state.veo_state import PageState
from state.state import AppState

@patch('pages.veo.requests.get')
@patch('pages.veo.requests.post')
@patch('mesop.state')
def test_veo_generation_flow_and_metadata(mock_state, mock_post, mock_get):
    """
    Tests the VEO generation flow, focusing on the UI state interaction,
    the API request creation, and handling the polling responses.
    """
    # --- Arrange ---
    prompt = "a test prompt for veo"

    # Setup mocked responses for HTTP requests
    mock_post_response = MagicMock()
    mock_post_response.json.return_value = {"job_id": "test_job_456", "status": "pending"}
    mock_post.return_value = mock_post_response

    mock_get_response = MagicMock()
    mock_get_response.json.return_value = {
        "job_id": "test_job_456",
        "status": "complete",
        "video_uris": ["gs://fake-bucket/fake_video.mp4"]
    }
    mock_get.return_value = mock_get_response

    # Setup the mocked AppState manually to avoid working outside request context
    mock_app_state = MagicMock(spec=AppState)
    mock_app_state.user_email = "test_user@example.com"
    mock_app_state.current_page = "veo"
    mock_app_state.session_id = "test_session_456"
    mock_app_state.sidenav_open = False
    mock_app_state.theme_mode = "dark"

    mock_page_state = PageState(
        veo_prompt_input=prompt,
        veo_model="2.0",
        aspect_ratio="16:9",
        video_length=5,
        resolution="720p",
        reference_image_gcs=None,
        last_reference_image_gcs=None,
        auto_enhance_prompt=False
    )

    # Configure the mock to return the correct state based on requested class
    def state_side_effect(state_class):
        if state_class == AppState:
            return mock_app_state
        return mock_page_state

    mock_state.side_effect = state_side_effect

    # --- Act ---
    # Call the event handler function. This is a generator function, so we need to exhaust it.
    for _ in on_click_veo(MagicMock()):
        pass

    # --- Assert ---
    # 1. Verify that our main POST API was called once with proper payload.
    mock_post.assert_called_once()
    post_kwargs = mock_post.call_args[1]
    assert "json" in post_kwargs
    payload = post_kwargs["json"]
    assert payload["prompt"] == prompt
    assert payload["model_version_id"] == "2.0"
    assert payload["duration_seconds"] == 5

    # 2. Verify that the polling was conducted
    mock_get.assert_called_once()
    get_args = mock_get.call_args[0]
    assert "test_job_456" in get_args[0]

    # 3. Inspect final PageState values after execution
    assert mock_page_state.is_loading is False
    assert mock_page_state.result_gcs_uris == ["gs://fake-bucket/fake_video.mp4"]
    assert len(mock_page_state.result_display_urls) == 1
    assert "fake_video.mp4" in mock_page_state.selected_video_url

    print("\nComponent-level integration test for VEO passed successfully.")
