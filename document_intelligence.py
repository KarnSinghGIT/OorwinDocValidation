from flask import Flask, render_template_string
import os
# from openai import AzureOpenAI
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import openai
from dotenv import load_dotenv
import re
import json

# Load environment variables
load_dotenv()

# Retrieve and validate environment variables
endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = 'gpt-3.5-turbo-0613'
client = openai.OpenAI()

# if not endpoint or not key or not openai_endpoint or not openai_api_key:
#     raise ValueError("Missing required environment variables for Azure services.")

# Create Azure clients
form_recognizer_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
# openai_client = AzureOpenAI(azure_endpoint=openai_endpoint, api_key=azure_openai_api_key, api_version="2024-02-15-preview")

def extract_entities(text):
    labels = [
    "Export_Authorisation_No", # Authorization number (e.g., "A-BCD-10292/2021", "M-XYZ-19812/2023")  
    "Exporter_Address",    # address(e.g., "Oniv Beverages Pvt Ltd At post Yedgaon, Taluka Junnar, Dist, Narayangaon, Maharashtra 410504", " Raghunathapur, Doddaballapur Rd, Bengaluru, Karnataka 561205")
    ]
    system_message= f"""
        You are an expert in Natural Language Processing. Your task is to identify common Named Entities (NER) in a given text.
        Provide factual data only.
        Do not pick fields from other entities.
        Do not make up by yourself.If entities(Export_Authorisation_No , Exporter_Address) are not present in text.fill emply value.
        The Named Entities (NER) types are exclusively: ({", ".join(labels)}).
        """
    assisstant_message=f"""
                        EXAMPLE:
                            [Text]: 'GOVERNMENT OF INDIA MINISTRY OF FINANCE (Department of Revenue) Central Bureau of Narcotics ORIGINAL - EXPORTER'S COPY (TO ACCOMPANY THE CONSIGNMENT) S. NO0033396 सत्यमेव जयते Authorisation for Official Approval of Export (The Narcotic Drugs and Psychotropic Substances Rules, 1985) Authorisation is not valid unless it bears official seal of the Issuing Authority hereon Export Authorisation No .: A-BCD-10292/2021 F.No.XVI/4/5589/Tech/Psy/2020 NARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India Exporter: XYZ Ltd., Pagna uptown Bangalore- India Consignee: Pharma Care International Pvt Ltd. Kathmandu-10, Baneshwor, Nepal, '
                            [Output]:{{
                                "Export_Authorisation_No": "A-BCD-10292/2021",
                                "Exporter_Address": "XYZ Ltd., Pagna uptown Bangalore- India"
                            }}
                            ###
                            [Text]: Authorisation for Official Approval of Export (The Narcotic Drugs and Psychotropic Substances Rules, 1985) Authorisation is not valid unless it bears official seal of the Issuing Authority hereon Export Authorisation No .:  F.No.XVI/4/5589/Tech/Psy/2020 NARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India Exporter: XYZ Ltd., Vijay Nagar Kanpur- India Consignee: Pharma Care International Pvt Ltd. Kathmandu-10, Baneshwor, Nepal, Port of Export: Raxaul, India Port of Entry: Kathmandu,
                            [Output]:{{
                                "Export_Authorisation_No": "",
                                "Exporter_Address": "XYZ Ltd., Vijay Nagar Kanpur- India"
                            }}
                            ###
                            [Text]: François is a Go developer. He mostly works as a freelancer but is open to any kind of job offering!
                            [Output]:{{
                                "Export_Authorisation_No": "",
                                "Exporter_Address": ""
                            }}
                        --"""
    user_message=f"""
                TASK:
                    [Text]: {text}
                """
    messages = [
          {"role": "system", "content": system_message},
          {"role": "assistant", "content": assisstant_message},
          {"role": "user", "content": user_message}
      ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        tools=generate_functions(labels),
        tool_choice={"type": "function", "function" : {"name": "enrich_entities"}}, 
        temperature=0,
        frequency_penalty=0,
        presence_penalty=0,
    )

    response_message = response.choices[0].message
    available_functions = {"enrich_entities": enrich_entities}  
    function_name = response_message.tool_calls[0].function.name
    
    function_to_call = available_functions[function_name]

    function_args = json.loads(response_message.tool_calls[0].function.arguments)

    function_response = function_to_call(text, function_args)

    # entities=response_message.content
    return function_response 
    # return [(page.page_number, ' '.join([line.content for line in page.lines])) for page in result.pages]

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using Azure Document Analysis."""
    with open(pdf_path, "rb") as pdf_file:
        poller = form_recognizer_client.begin_analyze_document("prebuilt-document", pdf_file)
        result = poller.result()
    return result.content
    # return [(page.page_number, ' '.join([line.content for line in page.lines])) for page in result.pages]

def enrich_entities(text: str, label_entities: dict) -> dict:
    """
    Enriches the data by extracting only Export_Authorisation_No and Exporter_Address fields.
    
    Parameters:
    text (str): The input text from which to extract entities.
    label_entities (dict): A dictionary to store the extracted entities.

    Returns:
    dict: A dictionary with the enriched entities.
    """
    # Define regular expressions to match the required fields
    export_authorisation_no_pattern = r"Export Authorisation No .:\s*([A-Z0-9-\/]+)"
    # exporter_address_pattern = r"Exporter:\s*(.*?)(?=Consignee|Port of Export|$)"
    # exporter_address_pattern = r"Exporter:\s*(.*?)\s*Consignee:"
    exporter_address_pattern = r"Exporter:\s*(.*?)\s*(?=Consignee|Port of Export|$)"

    # Search for the patterns in the text
    export_authorisation_no_match = re.search(export_authorisation_no_pattern, text, re.DOTALL)
    exporter_address_match = re.search(exporter_address_pattern, text, re.DOTALL)

    # Extract and store the matches in the label_entities dictionary
    if export_authorisation_no_match:
        label_entities["Export_Authorisation_No"] = export_authorisation_no_match.group(1).strip()
    if exporter_address_match:
        address = exporter_address_match.group(1).strip().replace('\n', ', ')
        label_entities["Exporter_Address"] = ' '.join(address.split())

    return label_entities
    
   
    
    return label_entities

def generate_functions(labels: dict) -> list:
    return [
        {   
            "type": "function",
            "function": {
                "name": "enrich_entities",
                "description": "Enrich Text with Knowledge Base Links",
                "parameters": {
                    "type": "object",
                        "properties": {
                            "r'^(?:' + '|'.join({labels}) + ')$'": 
                            {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            }
                        },
                        "additionalProperties": False
                },
            }
        }
    ]

# ===================================================================================
# File Validation Code Start Here
# ===================================================================================
def extract_text_from_pdf_only_first_page(pdf_path):
    """Extracts text from the first page of a PDF using Azure Document Analysis."""
    with open(pdf_path, "rb") as pdf_file:
        poller = form_recognizer_client.begin_analyze_document("prebuilt-document", pdf_file)
        result = poller.result()
    
    first_page = result.pages[0]
    first_page_text = ' '.join([line.content for line in first_page.lines])
    
    return first_page_text

def validate_document(template_path,input_path):
   
    template_texts = extract_text_from_pdf_only_first_page(template_path)
    input_texts = extract_text_from_pdf_only_first_page(input_path)
    
    system_message= f"""
        You are an expert in Natural Language Processing.
        your task is to Analyze the texts from two documents and provide if both have same format.
        First documnet is Template Document and Second document is Input Document.
        Do not compare the fields value.
        Provide factual data only.
        Provide "Document is compatible with Template." if both have same structure ohtherwise "Document is NOT compatible with Template."
        Do not make up by yourself.If can not figure it out just say 'I dont know'.
        """
    assisstant_message=f"""
                        EXAMPLE:
                            [Text from Template document]: 'Export Authorisation No .: P-EXP-10283/2021 F.No.XVI/4/5589/Tech/Psy/2020 NARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India Exporter: Umedica Laboratories Pvt. Ltd., Plot No. 221 G.I.D.C., Vapi-396 195 Gujarat- India '
                            [Text from Input document]: 'Export Authorisation No .: XYZ-PQRST F.No.XVI/4/5589/Tech/Psy/2020 NARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India Exporter: 280/5 Vijay Nagar Kanpur India '
                            [Output]: "Document is compatible with Template."
                            ###
                            [Text from Template document]: 'CONTOSO LTD., Contoso Headquarters, 123 456th St, New York, NY, 10001, Microsoft Corp, 123 Other St, Redmond, WA, 98052, INVOICE, INVOICE: INV-100, INVOICE DATE: 11/15/2019, DUE DATE: 12/15/2019, CUSTOMER NAME: MICROSOFT CORPORATION, SERVICE PERIOD: 10/14/2019 – 11/14/2019, CUSTOMER ID: CID-12345, BILL TO: Microsoft Finance, 123 Bill St, Redmond, WA, 98052, SHIP TO: Microsoft Delivery, 123 Ship St, Redmond, WA, 98052, SERVICE ADDRESS: Microsoft Services, 123 Service St, Redmond, WA, 98052'
                            [Text from Input document]: 'CONTOSO LTD., Contoso West Branch, 789 West St, San Francisco, CA, 94107, Alphabet Inc., 1600 Amphitheatre Parkway, Mountain View, CA, 94043, INVOICE, INVOICE: INV-200, INVOICE DATE: 02/25/2020, DUE DATE: 03/25/2020, CUSTOMER NAME: ALPHABET INC., SERVICE PERIOD: 01/14/2020 – 02/14/2020, CUSTOMER ID: CID-67890, BILL TO: Alphabet Finance, 1600 Billing St, Mountain View, CA, 94043, SHIP TO: Alphabet Delivery, 1600 Delivery St, Mountain View, CA, 94043, SERVICE ADDRESS: Alphabet Services, 1600 Service St, Mountain View, CA, 94043
 '
                            [Output]: "Document is compatible with Template."
                            ###
                            [Text from Template document]: '  Export Authorisation No .: P-EXP-10283/2021 F.No.XVI/4/5589/Tech/Psy/2020 NARCOTICS COMMISSIONER being the authority empowered to issue export authorisation under the Narcotic Drugs and Psychotropic Substances Rules, 1985 hereby authorises and permits the following exportation of Psychotropic Substances from India Exporter: Umedica Laboratories Pvt. Ltd., Plot No. 221 G.I.D.C., Vapi-396 195 Gujarat- India '
                            [Text from Input document]: '  CONTOSO LTD., Contoso South Branch, 123 South St, Austin, TX, 78701, Facebook, Inc., 1 Hacker Way, Menlo Park, CA, 94025, INVOICE, INVOICE: INV-400, INVOICE DATE: 08/20/2022, DUE DATE: 09/20/2022, CUSTOMER NAME: FACEBOOK, INC., SERVICE PERIOD: 07/20/2022 – 08/20/2022, CUSTOMER ID: CID-98765, BILL TO: Facebook Finance, 1 Finance Way, Menlo Park, CA, 94025, SHIP TO: Facebook Delivery, 1 Delivery Way, Menlo Park, CA, 94025, SERVICE ADDRESS: Facebook Services, 1 Service Way, Menlo Park, CA, 94025 '
                            [Output]:"Document is NOT compatible with Template."
                        --"""
    user_message=f"""
                TASK:
                    [Text from Template document]: {template_texts}, [Text from Input document]: {input_texts}
                """
    messages = [
          {"role": "system", "content": system_message},
          {"role": "assistant", "content": assisstant_message},
          {"role": "user", "content": user_message}
      ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=0,
        frequency_penalty=0,
        presence_penalty=0,
    )

    response_message = response.choices[0].message
    result =response_message.content
    return result