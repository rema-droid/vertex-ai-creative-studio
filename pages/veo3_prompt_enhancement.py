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

import time
import requests
import mesop as me

from common.analytics import track_click
from components.header import header
from components.page_scaffold import page_frame, page_scaffold
from state.veo3_prompt_enhancement_state import Veo3PromptEnhancementState
from state.state import AppState
from models.gemini import rewriter
from models.requests import VideoGenerationRequest
from config.default import Default
from config.rewriters import VEO3_ENHANCEMENT_PROMPT
from common.utils import create_display_url

cfg = Default()

STYLES = [
    "Cinematic",
    "Sci-Fi",
    "Action/High-Speed",
    "Nature/Drone",
    "Fantasy/Dreamy",
    "Hyper-Realistic"
]

@me.page(
    path="/veo3_prompt_enhancement",
    title="Veo 3 Prompt Enhancement",
)
def page():
    state = me.state(Veo3PromptEnhancementState)
    with page_scaffold(page_name="veo3_prompt_enhancement"):
        with page_frame():
            header("Veo 3 Prompt Enhancement", "movie_filter")

            with me.box(
                style=me.Style(
                    display="grid",
                    grid_template_columns="1fr 1fr",
                    gap=24,
                    padding=me.Padding.all(24),
                )
            ):
                # Left Column: Inputs
                with me.box(
                    style=me.Style(
                        display="flex",
                        flex_direction="column",
                        gap=16,
                        padding=me.Padding.all(16),
                        border_radius=8,
                        background="#fafafa" if me.theme_brightness() == "light" else "#212121",
                        border=me.Border.all(me.BorderSide(width=1, style="solid", color="#e0e0e0")),
                    )
                ):
                    me.text("Enhancement Controls", type="headline-6")

                    me.textarea(
                        label="Original Video Idea",
                        value=state.input_prompt,
                        on_input=on_input_prompt,
                        rows=5,
                        style=me.Style(width="100%"),
                    )

                    me.select(
                        label="Target Style",
                        options=[me.SelectOption(label=style, value=style) for style in STYLES],
                        value=state.selected_style,
                        on_selection_change=on_select_style,
                        style=me.Style(width="100%"),
                    )

                    with me.box(style=me.Style(display="flex", gap=8, margin=me.Margin(top=8))):
                        me.button(
                            "Enhance Prompt",
                            on_click=on_click_enhance,
                            type="raised",
                            disabled=state.is_enhancing or state.is_generating,
                        )

                        if state.enhanced_prompt:
                            me.button(
                                "Generate Video with Veo 3",
                                on_click=on_click_generate_video,
                                type="flat",
                                disabled=state.is_enhancing or state.is_generating,
                            )

                    if state.error_message:
                        with me.box(
                            style=me.Style(
                                margin=me.Margin(top=16),
                                padding=me.Padding.all(12),
                                border_radius=4,
                                background="#ffebee" if me.theme_brightness() == "light" else "#c62828",
                            )
                        ):
                            me.text(f"Error: {state.error_message}", style=me.Style(color="#d32f2f" if me.theme_brightness() == "light" else "#ffffff"))

                # Right Column: Outputs
                with me.box(
                    style=me.Style(
                        display="flex",
                        flex_direction="column",
                        gap=16,
                    )
                ):
                    # Enhanced Prompt Viewer
                    me.text("Enhanced Prompt", type="headline-6")
                    with me.box(
                        style=me.Style(
                            padding=me.Padding.all(16),
                            border_radius=8,
                            min_height=120,
                            background="#f5f5f5" if me.theme_brightness() == "light" else "#424242",
                            border=me.Border.all(me.BorderSide(width=1, style="solid", color="#e0e0e0")),
                            display="flex",
                            align_items="center",
                            justify_content="center" if not state.enhanced_prompt else "flex-start",
                        )
                    ):
                        if state.is_enhancing:
                            me.progress_spinner()
                        elif state.enhanced_prompt:
                            me.text(state.enhanced_prompt, style=me.Style(line_height=1.5))
                        else:
                            me.text("Enhanced prompt will appear here", style=me.Style(color="#757575"))

                    # Generated Video Player
                    me.text("Generated Video", type="headline-6")
                    with me.box(
                        style=me.Style(
                            padding=me.Padding.all(16),
                            border_radius=8,
                            min_height=300,
                            background="#f5f5f5" if me.theme_brightness() == "light" else "#424242",
                            border=me.Border.all(me.BorderSide(width=1, style="solid", color="#e0e0e0")),
                            display="flex",
                            align_items="center",
                            justify_content="center",
                        )
                    ):
                        if state.is_generating:
                            with me.box(style=me.Style(display="flex", flex_direction="column", align_items="center", gap=12)):
                                me.progress_spinner()
                                me.text(f"Generating video with Veo 3... Status: {state.job_status}", style=me.Style(color="#757575"))
                        elif state.generated_video_url:
                            me.video(
                                src=state.generated_video_url,
                                style=me.Style(width="100%", max_height=300, border_radius=8),
                                autoplay=True,
                                controls=True,
                            )
                        else:
                            me.text("Generated video will appear here", style=me.Style(color="#757575"))

def on_input_prompt(e: me.InputEvent):
    state = me.state(Veo3PromptEnhancementState)
    state.input_prompt = e.value

def on_select_style(e: me.SelectSelectionChangeEvent):
    state = me.state(Veo3PromptEnhancementState)
    state.selected_style = e.value

@track_click(element_id="veo3_enhance_prompt")
def on_click_enhance(e: me.ClickEvent):
    state = me.state(Veo3PromptEnhancementState)
    if not state.input_prompt:
        state.error_message = "Please enter an original video idea."
        yield
        return

    state.is_enhancing = True
    state.error_message = ""
    yield

    try:
        # Construct specific system prompt based on style
        formatted_system_prompt = VEO3_ENHANCEMENT_PROMPT + f"\nEnsure the video style is {state.selected_style}."
        rewritten = rewriter(state.input_prompt, formatted_system_prompt)
        state.enhanced_prompt = rewritten
    except Exception as ex:
        state.error_message = f"Failed to enhance prompt: {ex}"
    finally:
        state.is_enhancing = False
    yield

@track_click(element_id="veo3_generate_video")
def on_click_generate_video(e: me.ClickEvent):
    state = me.state(Veo3PromptEnhancementState)
    app_state = me.state(AppState)

    state.is_generating = True
    state.error_message = ""
    state.generated_video_url = ""
    state.job_status = "pending"
    yield

    # Construct VideoGenerationRequest
    request = VideoGenerationRequest(
        prompt=state.enhanced_prompt,
        duration_seconds=5,
        video_count=1,
        aspect_ratio="16:9",
        resolution="720p",
        enhance_prompt=False, # We enhanced it ourselves!
        model_version_id=cfg.VEO_MODEL_ID,
        person_generation="allow_all",
    )

    try:
        api_url = f"{cfg.API_BASE_URL}/api/veo/generate_async"
        headers = {"X-Goog-Authenticated-User-Email": app_state.user_email}

        response = requests.post(api_url, json=request.model_dump(), headers=headers)
        response.raise_for_status()
        data = response.json()

        state.current_job_id = data["job_id"]
        state.job_status = data["status"]
        yield
    except Exception as ex:
        state.error_message = f"Failed to start video generation: {ex}"
        state.is_generating = False
        yield
        return

    # Poll for completion
    while state.job_status in ["pending", "processing", "created"]:
        time.sleep(2)
        try:
            status_url = f"{cfg.API_BASE_URL}/api/veo/job/{state.current_job_id}"
            resp = requests.get(status_url)
            resp.raise_for_status()
            status_data = resp.json()
            state.job_status = status_data["status"]

            if state.job_status == "complete":
                video_uri = status_data.get("video_uri")
                video_uris = status_data.get("video_uris", [])
                selected_uri = video_uris[0] if video_uris else video_uri

                if selected_uri:
                    state.generated_video_url = create_display_url(selected_uri)
                else:
                    state.error_message = "No video URI returned from the completed job."
                state.is_generating = False
                yield
                break
            elif state.job_status == "failed":
                state.error_message = status_data.get("error_message", "Job failed on backend.")
                state.is_generating = False
                yield
                break
        except Exception as ex:
            state.error_message = f"Error while polling job status: {ex}"
            state.is_generating = False
            yield
            break
