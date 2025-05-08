# Instagram Follow Automation

A Python script that automates following Instagram users using Selenium WebDriver.

## ⚠️ Important Disclaimer

This script is for educational purposes only. Please use it responsibly and in accordance with Instagram's terms of service. Excessive automation may lead to account restrictions or bans.

## Features

- Automated Instagram login
- Bulk follow requests
- Handles pop-up dialogs
- Configurable user list
- Error handling and logging

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Instagram account

## Installation

1. Clone this repository:
```bash
git clone https://github.com/KrishSaraf/Insta-Follow-Automation.git
cd Insta-Follow-Automation
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Open `config.py` and update your Instagram credentials:
```python
INSTAGRAM_USERNAME = 'your_username'
INSTAGRAM_PASSWORD = 'your_password'
```

2. Edit the `usernames_to_follow` list in `config.py` with the accounts you want to follow.

## Usage

Run the script:
```bash
python instagram_follow.py
```

## Safety Features

- Random delays between actions to avoid detection
- Error handling for failed follow attempts
- Graceful browser cleanup

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 