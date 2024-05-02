#!/usr/bin/python
import time
import os
import json 

from neo4j import GraphDatabase

def print_summary(summary):
    if summary and summary.plan:
        print(summary.plan['args']['string-representation'])
    else:
        print("No Plan is used!")

def connector():
    CONN = "bolt://localhost:7687"
    AUTH = ("neo4j", "password")

    driver = GraphDatabase.driver(CONN, auth=AUTH)
    driver.verify_connectivity()

    return driver

def get_nodes(driver):
    query = "MATCH (n) RETURN n"

    print("Sending the query..")
    _, summary, _ = driver.execute_query(query)
    print("Back!..")

    print_summary(summary)

if __name__ == "__main__":
      driver = connector()
    try:
      get_nodes(driver)
    except Exception as error:
      driver.close()
      print(error)
