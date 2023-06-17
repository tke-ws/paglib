# paglib
RPA library using pyautogui

## Usage

### mouse click logging

```shell
python mouse_click_logger.py log.csv
```

### mouse replay

```python
from mouseplayer import MousePlayer
mp = MousePlayer()
mp.load_log("data/log.csv")
mp.replay()
```