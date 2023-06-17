from dataclasses import dataclass

@dataclass
class MouseData:
    """Set mouse information to be saved
    """
    x_in_window:float #0~1
    y_in_window:float # 0~1
    time_interval:float #[sec]
    title:str 