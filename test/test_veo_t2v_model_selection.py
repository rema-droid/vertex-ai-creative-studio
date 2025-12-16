

import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.veo import generate_video
from models.requests import VideoGenerationRequest
from config.default import Default

@patch('models.veo.client.models.generate_videos')
def test_t2v_uses_veo3_fast_model(mock_generate_videos):
    """Tests that generate_video uses the Veo 3.0 Fast endpoint when model is '3.0-fast'."""
    cfg = Default()
    request = VideoGenerationRequest(
        model_version_id="3.0-fast",
        prompt="A test prompt",
        aspect_ratio="16:9",
        video_count=1,
        duration_seconds=5,
        resolution="1080p",
        enhance_prompt=False,
        person_generation="allow_all",
        seed=123,
    )
    generate_video(request)
    mock_generate_videos.assert_called_once()
    called_model = mock_generate_videos.call_args[1]['model']
    assert cfg.VEO_EXP_FAST_MODEL_ID in called_model

@patch('models.veo.client.models.generate_videos')
def test_t2v_uses_veo3_model(mock_generate_videos):
    """Tests that generate_video uses the Veo 3.0 endpoint when model is '3.0'."""
    cfg = Default()
    request = VideoGenerationRequest(
        model_version_id="3.0",
        prompt="A test prompt",
        aspect_ratio="16:9",
        video_count=1,
        duration_seconds=5,
        resolution="1080p",
        enhance_prompt=False,
        person_generation="allow_all"
    )
    generate_video(request)
    mock_generate_videos.assert_called_once()
    called_model = mock_generate_videos.call_args[1]['model']
    assert cfg.VEO_EXP_MODEL_ID in called_model

@patch('models.veo.client.models.generate_videos')
def test_t2v_uses_veo2_model(mock_generate_videos):
    """Tests that generate_video uses the Veo 2.0 endpoint when model is '2.0'."""
    cfg = Default()
    request = VideoGenerationRequest(
        model_version_id="2.0",
        prompt="A test prompt",
        aspect_ratio="16:9",
        video_count=1,
        duration_seconds=5,
        resolution="1080p",
        enhance_prompt=False,
        person_generation="allow_all"
    )
    generate_video(request)
    mock_generate_videos.assert_called_once()
    called_model = mock_generate_videos.call_args[1]['model']
    assert cfg.VEO_MODEL_ID in called_model

