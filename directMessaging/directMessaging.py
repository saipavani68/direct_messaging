#!/usr/bin/env python3

# See <https://code-maven.com/using-templates-in-flask>
from flask import Flask, request, jsonify, g
import logging
from dynamodb_operations import create_movie_table, create_items

app = Flask(__name__)

@app.cli.command('init')
def init_db():
    app.logger.info('inside direct messaging')
    with app.app_context():
       direct_mesages_table = create_movie_table()
       app.logger.info("Table status:", direct_mesages_table.table_status)
       create_items(direct_mesages_table)