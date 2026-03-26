from fastapi import FastAPI, HTTPException, Query
from database import products_collection
from models import Product
import requests

app = FastAPI(title="Inventory Management API")