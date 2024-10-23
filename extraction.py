"""
This code sample shows Prebuilt Document operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Form Recognizer Python client library SDKs
https://learn.microsoft.com/azure/applied-ai-services/form-recognizer/quickstarts/get-started-v3-sdk-rest-api?view=doc-intel-3.1.0&pivots=programming-language-python
"""


from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import os
import io
from dotenv import load_dotenv
"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""



async def analyze_document(file):
    
    load_dotenv()
    endpoint =os.getenv("ENDPOINT")
    key = os.getenv("KEY")

    if not key:
        raise ValueError("API key (KEY) is missing or not set properly.")
    
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    print("test")
    # Convert the uploaded file to bytes
    file_bytes = file.read()
    
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout", document=io.BytesIO(file_bytes)
    )
    result =  poller.result()

    analysis_text = []
    
    if hasattr(result, 'paragraphs'):
        analysis_text.append("\n## Paragraphen\n")
        for paragraph in result.paragraphs:
            analysis_text.append(paragraph.content)
            
    
    if hasattr(result, 'tables'):
        for idx, table in enumerate(result.tables):
            analysis_text.append(f"\n## Tabellen {idx + 1}\n")
            rows = [[] for _ in range(table.row_count)]
            for cell in table.cells:
                rows[cell.row_index].append(cell.content)
            headers = rows.pop(0)  # Assume the first row is the header
            analysis_text.append(" | ".join(headers))
            analysis_text.append(" | ".join(["---" for _ in headers]))
            for row in rows:
                analysis_text.append(" | ".join(row))
    
    if hasattr(result, 'key_value_pairs'):
        analysis_text.append("## Schlüssel-Wert-Paar\n")
        for kv_pair in result.key_value_pairs:
            if kv_pair.key and kv_pair.value:
                analysis_text.append(f"**{kv_pair.key.content}**: {kv_pair.value.content}\n")
            elif kv_pair.key:
                analysis_text.append(f"**{kv_pair.key.content}**: None\n")
       
    
    return "\n".join(analysis_text)

