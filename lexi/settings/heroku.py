import os

from .base import *
from .utils import *
from .users import *

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ['DEBUG']
