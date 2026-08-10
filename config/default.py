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

import json
import os
from dataclasses import dataclass, field
from typing import TypedDict

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(override=True)


# Define ImageModel here
class ImageModel(TypedDict):
    """Defines Models For Image Generation."""

    display: str
    model_name: str


class NavItem(BaseModel):
    id: int
    display: str
    icon: str
    route: str | None = None
    group: str | None = None
    align: str | None = None
    feature_flag: str | None = None
    feature_flag_not: str | None = None
    description: str | None = None
    video_url: str | None = None
    video_object_position: str | None = None


class NavConfig(BaseModel):
    pages: list[NavItem]


@dataclass
class Default:
    """Defaults class"""

    VERSION: str = "1.3.16"  # Gemini Writers Studio config
    APP_ENV: str = os.environ.get("APP_ENV", "")
    APP_TITLE: str = os.environ.get("APP_TITLE", "GenMedia Creative Studio")
    BRAND_NAME: str = os.environ.get("BRAND_NAME", "GENMEDIA STUDIO")
    APP_SUBTITLE: str = os.environ.get(
        "APP_SUBTITLE",
        "Fuel your creativity with Google Cloud Vertex AI's generative media models and custom workflows.",
    )
    API_BASE_URL: str = os.environ.get(
        "API_BASE_URL",
        f"http://localhost:{os.environ.get('PORT', '8080')}",
    )

    SERVICE_ACCOUNT_EMAIL: str = os.environ.get("SERVICE_ACCOUNT_EMAIL")
    # Gemini
    PROJECT_ID: str = os.environ.get("PROJECT_ID")
    LOCATION: str = os.environ.get("LOCATION", "us-central1")
    GA_MEASUREMENT_ID: str = os.environ.get("GA_MEASUREMENT_ID")
    MODEL_ID: str = os.environ.get("MODEL_ID", "gemini-2.5-flash")
    INIT_VERTEX: bool = True
    GEMINI_IMAGE_GEN_MODEL: str = os.environ.get(
        "GEMINI_IMAGE_GEN_MODEL",
        "gemini-2.5-flash-image",
    )
    GEMINI_IMAGE_GEN_LOCATION: str = os.environ.get(
        "GEMINI_IMAGE_GEN_LOCATION",
        "global",
    )
    GEMINI_IMAGE_GEN_API_BASE_URL: str | None = os.environ.get(
        "GEMINI_IMAGE_GEN_API_BASE_URL",
    )

    GEMINI_AUDIO_ANALYSIS_MODEL_ID: str = os.environ.get(
        "GEMINI_AUDIO_ANALYSIS_MODEL_ID",
        "gemini-2.5-flash",
    )
    GEMINI_WRITERS_WORKSHOP_MODEL_ID: str = os.environ.get(
        "GEMINI_WRITERS_WORKSHOP_MODEL_ID",
        MODEL_ID,
    )

    # Collections
    GENMEDIA_FIREBASE_DB: str = os.environ.get("GENMEDIA_FIREBASE_DB", "(default)")
    GENMEDIA_COLLECTION_NAME: str = os.environ.get(
        "GENMEDIA_COLLECTION_NAME",
        "genmedia",
    )
    SESSIONS_COLLECTION_NAME: str = os.environ.get(
        "SESSIONS_COLLECTION_NAME",
        "sessions",
    )

    # storage
    GENMEDIA_BUCKET: str = os.environ.get("GENMEDIA_BUCKET", f"{PROJECT_ID}-assets")
    VIDEO_BUCKET: str = os.environ.get("VIDEO_BUCKET", f"{PROJECT_ID}-assets/videos")
    IMAGE_BUCKET: str = os.environ.get("IMAGE_BUCKET", f"{PROJECT_ID}-assets/images")
    GCS_ASSETS_BUCKET: str = os.environ.get("GCS_ASSETS_BUCKET")

    # Library
    LIBRARY_MEDIA_PER_PAGE: int = int(os.environ.get("LIBRARY_MEDIA_PER_PAGE", 15))

    # Veo
    VEO_MODEL_ID: str = os.environ.get("VEO_MODEL_ID", "veo-3.1-fast-generate-001")
    VEO_PROJECT_ID: str = os.environ.get("VEO_PROJECT_ID", PROJECT_ID)

    VEO_EXP_MODEL_ID: str = os.environ.get(
        "VEO_EXP_MODEL_ID", "veo-3.1-generate-preview"
    )
    VEO_EXP_FAST_MODEL_ID: str = os.environ.get(
        "VEO_EXP_FAST_MODEL_ID",
        "veo-3.1-fast-generate-preview",
    )
    VEO_EXP_PROJECT_ID: str = os.environ.get("VEO_EXP_PROJECT_ID", PROJECT_ID)

    # VTO
    VTO_LOCATION: str = os.environ.get("VTO_LOCATION", "us-central1")
    VTO_MODEL_ID: str = os.environ.get("VTO_MODEL_ID", "virtual-try-on-preview-08-04")
    GENMEDIA_VTO_MODEL_COLLECTION_NAME: str = os.environ.get(
        "GENMEDIA_VTO_MODEL_COLLECTION_NAME",
        "genmedia-vto-model",
    )
    GENMEDIA_VTO_CATALOG_COLLECTION_NAME: str = os.environ.get(
        "GENMEDIA_VTO_CATALOG_COLLECTION_NAME",
        "genmedia-vto-catalog",
    )

    # Temperatures for Character Consistency Workflow
    # Low temp for factual, structured output. Increasing may break JSON parsing.
    TEMP_FORENSIC_ANALYSIS: float = 0.1
    # Low temp for direct, non-creative translation of data to text.
    TEMP_DESCRIPTION_TRANSLATION: float = 0.1
    # Mid-range temp for creative but controlled prompt engineering.
    TEMP_SCENE_GENERATION: float = 0.3
    # Low temp for analytical comparison and structured JSON output.
    TEMP_BEST_IMAGE_SELECTION: float = 0.2

    # Character Consistency
    CHARACTER_CONSISTENCY_IMAGEN_MODEL: str = "imagen-3.0-capability-001"
    CHARACTER_CONSISTENCY_VEO_MODEL: str = os.environ.get(
        "CHARACTER_CONSISTENCY_VEO_MODEL",
        "veo-3.0-fast-generate-001",
    )
    CHARACTER_CONSISTENCY_GEMINI_MODEL: str = os.environ.get(
        "CHARACTER_CONSISTENCY_GEMINI_MODEL",
        MODEL_ID,
    )

    # Lyria
    LYRIA_LOCATION: str = os.environ.get("LYRIA_LOCATION", "us-central1")
    LYRIA_MODEL_VERSION: str = os.environ.get("LYRIA_MODEL_VERSION", "lyria-002")
    LYRIA_PROJECT_ID: str = os.environ.get("LYRIA_PROJECT_ID", PROJECT_ID)
    MEDIA_BUCKET: str = os.environ.get("MEDIA_BUCKET", f"{PROJECT_ID}-assets")

    # Imagen
    MODEL_IMAGEN2 = "imagegeneration@006"
    MODEL_IMAGEN_NANO = "imagegeneration@004"
    MODEL_IMAGEN = "imagen-3.0-generate-002"
    MODEL_IMAGEN_FAST = "imagen-3.0-fast-generate-001"
    MODEL_IMAGEN4 = "imagen-4.0-generate-001"
    MODEL_IMAGEN4_FAST = "imagen-4.0-fast-generate-001"
    MODEL_IMAGEN4_ULTRA = "imagen-4.0-ultra-generate-001"
    MODEL_IMAGEN_EDITING = "imagen-3.0-capability-001"
    MODEL_IMAGEN_PRODUCT_RECONTEXT: str = os.environ.get(
        "MODEL_IMAGEN_PRODUCT_RECONTEXT",
        "imagen-product-recontext-preview-06-30",
    )

    IMAGEN_GENERATED_SUBFOLDER: str = os.environ.get(
        "IMAGEN_GENERATED_SUBFOLDER",
        "generated_images",
    )
    IMAGEN_EDITED_SUBFOLDER: str = os.environ.get(
        "IMAGEN_EDITED_SUBFOLDER",
        "edited_images",
    )

    IMAGEN_PROMPTS_JSON = "prompts/imagen_prompts.json"

    USE_MEDIA_PROXY: bool = os.environ.get("USE_MEDIA_PROXY", "true").lower() == "true"

    image_modifiers: list[str] = field(
        default_factory=lambda: [
            "aspect_ratio",
            "content_type",
            "color_tone",
            "lighting",
            "composition",
        ],
    )


def get_welcome_page_config():
    with open("config/navigation.json") as f:
        data = json.load(f)

    # This will raise a validation error if the JSON is malformed
    config = NavConfig(**data)

    def is_feature_enabled(page: NavItem):
        if page.feature_flag:
            return bool(getattr(Default, page.feature_flag, False))
        if page.feature_flag_not:
            return not bool(getattr(Default, page.feature_flag_not, False))
        return True

    filtered_pages = [
        page.model_dump(exclude_none=True)
        for page in config.pages
        if is_feature_enabled(page)
    ]

    return sorted(filtered_pages, key=lambda x: x["id"])


def load_about_page_config():
    env = os.environ.get("APP_ENV")  # e.g., 'local', 'dev', 'prod'
    env_config_path = f"config/about_content.{env}.json"
    default_config_path = "config/about_content.json"

    config_path = None
    if env and os.path.exists(env_config_path):
        config_path = env_config_path
    elif os.path.exists(default_config_path):
        config_path = default_config_path
    else:
        # Neither the environment-specific nor the default file was found
        return None

    try:
        with open(config_path) as f:
            content_str = f.read()
            # Replace hardcoded branding dynamically with the configured values
            content_str = content_str.replace(
                "GenMedia Creative Studio",
                os.environ.get("APP_TITLE", "GenMedia Creative Studio"),
            )
            content_str = content_str.replace(
                "GENMEDIA STUDIO", os.environ.get("BRAND_NAME", "GENMEDIA STUDIO")
            )
            content = json.loads(content_str)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

    # The rest of the function that processes GCS URLs remains the same
    bucket_name = Default.GCS_ASSETS_BUCKET
    if not bucket_name:
        return content

    base_url = f"https://storage.googleapis.com/{bucket_name}"

    for section in content.get("sections", []):
        if section.get("image"):
            section["image"] = f"{base_url}/{section['image']}"
        if section.get("video"):
            section["video"] = f"{base_url}/{section['video']}"

    return content


ABOUT_PAGE_CONTENT = load_about_page_config()
