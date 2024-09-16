
# THIS DOES NOT WORK AS OF UPLOAD! DO NOT RUN

# uta class sniper

This project was inspired by [a class notifier made for UT Austin](https://github.com/christiandipert/UT-Course-Availability-Tracker).

Are you tired of the rush to secure classes on time? Want an easier way to sign up for classes without having to navigate MyMav's horrid interface? This is the perfect repo for you!

## usage

To get started, first install the dependencies required for the script:
```python
pip install -r requirements.txt
```

Then, make a file called ```credentials.py``` and fill it in using the template below. This data is only sent to the login page, and is not used anywhere else.
```python
USERNAME = "(uta email, for example xxx1234@mavs.uta.edu)"
PASSWORD = "(uta password)"
```

To run, simply open command line and type:
```python
python main.py
```
## features

- Microsoft Authenticator Compatibility
- Allows you to check class sizes and openings

## features in the works

- SMS 2FA Compatibility
- Integrated Class Sniper
- Discord Webhook Functionality 
- Desktop app down the line

