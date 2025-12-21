

import pytest
from models.veo import generate_video
from models.requests import VideoGenerationRequest
from config.veo_models import VEO_MODELS

# Parametrize the test to run for each model defined in the configuration.
@pytest.mark.integration
@pytest.mark.parametrize("model_config", VEO_MODELS)
def test_veo_t2v_api_call(gcs_bucket_for_tests, model_config):
    """An integration test that calls the real VEO API for text-to-video.
    
    This test is marked as 'integration' and will be skipped unless explicitly
    run with 'pytest -m integration'. It verifies that the application can
    successfully communicate with the live VEO API and receive a valid response
    for every supported model.
    """
    # --- Arrange ---
    # Use a simple, reliable prompt that is unlikely to trigger content filters.
    prompt = "a happy dog running on a sunny beach"
    output_gcs = f"{gcs_bucket_for_tests}/integration_tests"

    request = VideoGenerationRequest(
        prompt=prompt,
        duration_seconds=model_config.default_duration,
        video_count=model_config.default_samples,
        aspect_ratio=model_config.supported_aspect_ratios[0],
        resolution=model_config.default_resolution,
        enhance_prompt=model_config.supports_prompt_enhancement,
        model_version_id=model_config.version_id,
        person_generation="allow_all",
        seed=42,
    )

    # --- Act ---
    video_uris, resolution = generate_video(request)

    # --- Assert ---
    assert video_uris is not None, "The API operation result should not be None."
    assert len(video_uris) > 0, "The 'video_uris' list should not be empty."
    assert resolution == model_config.default_resolution, "The resolution should match the request."

    for uri in video_uris:
        assert uri.startswith(f"gs://{output_gcs}"), f"The video URI should be in the specified output bucket. Got {uri}"

    print(f"\nIntegration test for model {model_config.version_id} PASSED. Video generated successfully at: {video_uris[0]}")

