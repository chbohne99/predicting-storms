import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from CLASSML.preprocessing import preprocessing
from CLASSML.registry import load_model
import numpy as np
