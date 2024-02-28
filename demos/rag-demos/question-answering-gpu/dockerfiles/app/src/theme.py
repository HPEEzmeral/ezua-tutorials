from typing import Union

from gradio.themes import Base
from gradio.themes.utils import colors


WHITE = "#FFFFFF"
BACKGOUND_COLOR_DARK = "#374151"
HPE_PRIMARY_COLOR = "#01A982"
HPE_PRIMARY_COLOR_DARK = "#008567"
HPE_TEXT_COLOR_SECONDARY = "#444444"

BORDER_WIDTH = "3px"
BORDER_RADIUS = "100px"
INPUT_BORDER_WIDTH = "1px"


class EzmeralTheme(Base):
    def __init__(
            self,
            *,
            primary_hue: Union[colors.Color, str] = colors.emerald,
            neutral_hue: Union[colors.Color, str] = colors.gray,
            ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=primary_hue,
            neutral_hue=neutral_hue
        )
        
        super().set(
            button_border_width=BORDER_WIDTH,
            button_border_width_dark=BORDER_WIDTH,
            button_primary_background_fill=HPE_PRIMARY_COLOR,
            button_primary_background_fill_dark=BACKGOUND_COLOR_DARK,
            button_primary_text_color=WHITE,
            button_primary_border_color=HPE_PRIMARY_COLOR,
            button_primary_border_color_dark=HPE_PRIMARY_COLOR,
            button_primary_border_color_hover=HPE_PRIMARY_COLOR_DARK,
            button_primary_border_color_hover_dark=HPE_PRIMARY_COLOR_DARK,
            button_primary_background_fill_hover=HPE_PRIMARY_COLOR_DARK,
            button_large_radius=BORDER_RADIUS,
            button_secondary_background_fill=WHITE,
            button_secondary_background_fill_dark=BACKGOUND_COLOR_DARK,
            button_secondary_border_color_hover=HPE_PRIMARY_COLOR_DARK,
            button_secondary_border_color_hover_dark=HPE_PRIMARY_COLOR,
            button_secondary_border_color=HPE_PRIMARY_COLOR,
            button_secondary_border_color_dark=BACKGOUND_COLOR_DARK,
            button_secondary_text_color=HPE_TEXT_COLOR_SECONDARY,
            slider_color=HPE_PRIMARY_COLOR,
            # slider_color_dark=HPE_PRIMARY_COLOR,
            checkbox_border_color_hover=HPE_PRIMARY_COLOR,
            checkbox_border_color_hover_dark=HPE_PRIMARY_COLOR,
            input_border_width=INPUT_BORDER_WIDTH,
            input_border_width_dark=INPUT_BORDER_WIDTH,
            input_border_color_focus=HPE_PRIMARY_COLOR,
            input_border_color_focus_dark=HPE_PRIMARY_COLOR,
            input_border_color_hover=HPE_PRIMARY_COLOR,
            input_border_color_hover_dark=HPE_PRIMARY_COLOR
            )
