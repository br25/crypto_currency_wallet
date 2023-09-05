# Tryout Task (ASETT)

This Django project allows users to manage their cryptocurrency portfolios. It utilizes cryptocurrency API calls to gather data and provides various functionalities. Below, you'll find an overview of the project, installation instructions, and other important details.


## Overview

As part of Ayulla's Software Engineering Tryout Task (ASETT), this project focuses on implementing the following features:

1. **User Authentication**:
   - Sign up, log in, and log out of the system.
   - Password recovery features.
   - Securely storing and hashing passwords using Django's authentication system.

2. **Referral System**:
   - Users can invite others to join the platform via a referral link.
   - Tracking of referral links, with referrers receiving bonuses when new users sign up using their link.

3. **Crypto-Currency Wallets**:
   - Users can add and remove cryptocurrencies to/from their wallet.
   - Each cryptocurrency includes a name, symbol, current price, and quantity in the user's portfolio.
   - Users can view a detailed portfolio, showing the value of each cryptocurrency and the total portfolio value.

4. **Homepage**:
   - Displays 24-hour price and percentage change of the top 10 ranked cryptocurrencies.
   - Includes 24-hour price and percentage change of the user's portfolio.
   - Provides a search bar for users to add new cryptocurrencies to their portfolio.

## Installation

Follow these steps to set up and run the project locally:

1. Clone the repository:
    ```bash
    https://github.com/br25/crypto_currency_wallet.git
    ```

2.  * python -m venv venv
    * source venv/bin/activate

3. pip install -r requirements.txt

4. python manage.py makemigrations

5. python manage.py migrate

6. python manage.py createsuperuser

7. python manage.py runserver


## API

1. http://127.0.0.1:8000/auth/signup/

2. http://127.0.0.1:8000/auth/login/

3. http://127.0.0.1:8000/auth/logout/

4. http://127.0.0.1:8000/auth/password-reset/

5. http://127.0.0.1:8000/api

6. http://127.0.0.1:8000/api/search/

7. http://127.0.0.1:8000/api/portfolio/

8. http://127.0.0.1:8000/api/referral/

9. http://127.0.0.1:8000/remove-crypto/<str:currency_id>/