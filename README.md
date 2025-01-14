# Brighton Bot

A Streamlit-based web application for automating parking reservations at Brighton Resort using Selenium WebDriver.

## Description

Brighton Bot automates the process of reserving parking spots at Brighton Resort through the Honk mobile platform. It features a user-friendly web interface built with Streamlit and uses Selenium for web automation.

## Prerequisites

Before using the bot, ensure you have:
1. A Honk mobile account
2. Saved credit card information at [Honk Payment Cards](https://parking.honkmobile.com/payment-cards)
3. Only one license plate saved at [Honk Vehicles](https://parking.honkmobile.com/vehicles)
4. Python 3.7 or higher installed
5. Chrome browser installed
6. ChromeDriver compatible with your Chrome version

## Installation

1. Clone the repository: 
   ```bash
   git clone <repository-url>
   cd brighton-bot
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables in a `.env` file:
   ```bash
   HONK_USERNAME=<your_honk_username>
   HONK_PASSWORD=<your_honk_password>
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run main_v4_streamlit_working.py
   ```
5. Update the ChromeDriver path in the code to match your system's path.

## Usage

1. In the web interface:
   - Enter your Honk mobile email
   - Enter your Honk mobile password
   - Specify the target date (day of month)
   - Set maximum attempts and sleep duration
   - Click "Start Reservation"
2. Alternatively, run the script directly from the command line:
   ```bash
   python main_v4_streamlit_working.py
   ```

## Important Notes

- The bot will automatically attempt to reserve a 4+ Carpool spot
- The default price is set to $10.00
- Make sure your ChromeDriver is compatible with your Chrome browser version
- The bot includes error handling and multiple click attempt methods for reliability


## Disclaimer

This bot is for educational purposes only. Please use responsibly and in accordance with Brighton Resort's terms of service.
