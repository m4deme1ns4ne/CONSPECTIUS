from .handling import GPTResponse
from .logger import logger
from app.core.promts_for_gpt.max_promt import beginning_text, middle_of_the_text, end_of_text
# from app.core.promts_for_gpt.middle_promt import first_part, second_part
# from app.core.promts_for_gpt.min_promt import whole_part
from .states import MainState
from .transcribing import transcribing_aai


__all__ = [
    "GPTResponse",
    "logger",
    "beginning_text",
    "middle_of_the_text",
    "end_of_text",
    "MainState",
    "transcribing_aai"
]
