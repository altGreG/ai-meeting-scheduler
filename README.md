# Python environment configuration

## Create and enter virtual environment
```bash
pip install virtualenv 
python -m venv env
# enter created virtual environment
env\Scripts\activate
```

## Download software needed for creawai
1. Go to: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Download installer
3. Go to Individual components label and download these two things:
    - MSVC version 143 - VS 2022 C++ x64/x86 build tools (latest)
    - Windows 11 SDK(10.0.ver_nr.0)

## Download Python dependencies
```bash
pip install crewai crewai-tools
pip install google-auth google-auth-oauthlib google-api-python-client
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```
