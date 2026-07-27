# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import sys
from unittest.mock import MagicMock, patch

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from common.error_handling import GenerationError
from models.requests import VideoGenerationRequest, APIReferenceImage
from models.veo import generate_video

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@patch("models.veo.client")
def test_veo_extension_pipeline(mock_client):
    """
    Test the Veo video extension capability pipeline using mocked GenAI client.
    """
    # Mock the return value of client.models.generate_videos
    mock_operation = MagicMock()
    mock_operation.done = True
    mock_operation.error = None

    mock_video = MagicMock()
    mock_video.video.uri = "gs://fake-bucket/extended_video.mp4"

    mock_result = MagicMock()
    mock_result.rai_media_filtered_count = 0
    mock_result.generated_videos = [mock_video]

    mock_operation.result = mock_result
    mock_operation.response = MagicMock()
    mock_client.models.generate_videos.return_value = mock_operation

    # Create a request with video extension fields
    request = VideoGenerationRequest(
        prompt="A continuation of the scene, cinematic lighting",
        model_version_id="3.1-fast-preview",  # Maps to config
        aspect_ratio="16:9",
        resolution="720p",
        duration_seconds=7,
        video_count=1,
        enhance_prompt=False,
        person_generation="allow_all",
        video_input_gcs="gs://genai-blackbelt-fishfooding-assets/videos/flower.mp4",
        video_input_mime_type="video/mp4",
    )

    video_uris, resolution = generate_video(request)

    # Verify that mock_client.models.generate_videos was called with correct parameters
    mock_client.models.generate_videos.assert_called_once()
    call_kwargs = mock_client.models.generate_videos.call_args[1]

    assert call_kwargs["prompt"] == request.prompt
    assert call_kwargs["video"] is not None
    assert call_kwargs["video"].uri == "gs://genai-blackbelt-fishfooding-assets/videos/flower.mp4"
    assert call_kwargs["video"].mime_type == "video/mp4"
    assert video_uris == ["gs://fake-bucket/extended_video.mp4"]
    assert resolution == "720p"


@patch("models.veo.client")
def test_veo_text_to_video_pipeline(mock_client):
    """
    Test the standard text-to-video generation pipeline using mocked GenAI client.
    """
    mock_operation = MagicMock()
    mock_operation.done = True
    mock_operation.error = None

    mock_video = MagicMock()
    mock_video.video.uri = "gs://fake-bucket/generated_t2v.mp4"

    mock_result = MagicMock()
    mock_result.rai_media_filtered_count = 0
    mock_result.generated_videos = [mock_video]

    mock_operation.result = mock_result
    mock_operation.response = MagicMock()
    mock_client.models.generate_videos.return_value = mock_operation

    request = VideoGenerationRequest(
        prompt="A cute cat playing with a toy",
        model_version_id="3.1-fast-preview",
        aspect_ratio="16:9",
        resolution="720p",
        duration_seconds=5,
        video_count=1,
        enhance_prompt=True,
        person_generation="allow_all"
    )

    video_uris, resolution = generate_video(request)

    mock_client.models.generate_videos.assert_called_once()
    call_kwargs = mock_client.models.generate_videos.call_args[1]

    assert call_kwargs["prompt"] == request.prompt
    assert call_kwargs["video"] is None
    assert call_kwargs["image"] is None
    assert video_uris == ["gs://fake-bucket/generated_t2v.mp4"]


@patch("models.veo.client")
def test_veo_r2v_pipeline(mock_client):
    """
    Test the reference-to-video (R2V) style and asset pipeline.
    """
    mock_operation = MagicMock()
    mock_operation.done = True
    mock_operation.error = None

    mock_video = MagicMock()
    mock_video.video.uri = "gs://fake-bucket/generated_r2v.mp4"

    mock_result = MagicMock()
    mock_result.rai_media_filtered_count = 0
    mock_result.generated_videos = [mock_video]

    mock_operation.result = mock_result
    mock_operation.response = MagicMock()
    mock_client.models.generate_videos.return_value = mock_operation

    request = VideoGenerationRequest(
        prompt="A video matching this style and asset",
        model_version_id="3.1-fast-preview",
        aspect_ratio="16:9",
        resolution="720p",
        duration_seconds=5,
        video_count=1,
        enhance_prompt=True,
        person_generation="allow_all",
        r2v_style_image=APIReferenceImage(gcs_uri="gs://bucket/style.png", mime_type="image/png"),
        r2v_references=[APIReferenceImage(gcs_uri="gs://bucket/asset.png", mime_type="image/png")]
    )

    video_uris, resolution = generate_video(request)

    mock_client.models.generate_videos.assert_called_once()
    call_kwargs = mock_client.models.generate_videos.call_args[1]

    # Check reference images were processed
    config_args = call_kwargs["config"]
    assert config_args is not None
    assert len(video_uris) == 1
    assert video_uris == ["gs://fake-bucket/generated_r2v.mp4"]
