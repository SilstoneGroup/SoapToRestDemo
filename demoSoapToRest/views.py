import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from demoSoapToRest.params import *
from zeep import Client
import xml.etree.ElementTree as ET
from demoSoapToRest.settings import BASE_DIR

file_name = "response.xml"


@api_view(["GET"])
def list_currencies(request):
    response = dict()
    client = Client(os.path.join(BASE_DIR, "demoSoapToRest", "wsdl", "sample.wsdl"))
    result = client.service.ListCurrencies(
        parms_in=dict({"api_username": API_USERNAME, "api_key": API_KEY, "api_password": API_PASSWORD}))
    if result.ResultCode == 0:
        f = open(file_name, "w")
        f.write(result.Results)
        f.close()
    response["Currencies"] = []
    response["Currencies"].append(parse_response())
    # return Response(dict({"result": "success"}))
    return Response(response)


def parse_response():
    tree = ET.parse(file_name)
    cur = tree.find("Currency")
    return dict({"code": cur.find("Code").text,
                 "name": cur.find("Name").text})

