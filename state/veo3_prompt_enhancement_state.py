import mesop as me

@me.stateclass
class Veo3PromptEnhancementState:
    input_prompt: str = ""
    enhanced_prompt: str = ""
    selected_style: str = "Cinematic"
    is_enhancing: bool = False
    is_generating: bool = False
    generated_video_url: str = ""
    error_message: str = ""
    show_error_dialog: bool = False
    current_job_id: str = ""
    job_status: str = ""
