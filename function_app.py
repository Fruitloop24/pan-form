import logging
import azure.functions as func
import requests
import os
import json

# Initialize the function app
app = func.FunctionApp()

# Get blob URL from environment variable
ANALYSIS_BLOB_URL = os.getenv("ANALYSIS_BLOB_URL", "https://panstorage.blob.core.windows.net/open/analysis.json")

def create_form_html(data):
    """Create a styled, editable form from the analysis data"""
    return f"""
    <div class="editable-fields">
        <h2 class="text-2xl font-bold mb-6">Receipt Details</h2>
        
        <div class="grid gap-4">
            <div class="form-group">
                <label for="vendor" class="text-green-700 font-medium">Vendor Name:</label>
                <input id="vendor" type="text" value="{data['vendor_name']}" 
                       class="w-full p-2 border rounded focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="form-group">
                <label for="address" class="text-green-700 font-medium">Address:</label>
                <input id="address" type="text" value="{data['address']}"
                       class="w-full p-2 border rounded focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="form-group">
                <label for="phone" class="text-green-700 font-medium">Phone:</label>
                <input id="phone" type="text" value="{data['phone']}"
                       class="w-full p-2 border rounded focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="form-group">
                <label for="date" class="text-green-700 font-medium">Date:</label>
                <input id="date" type="date" value="{data['date']}"
                       class="w-full p-2 border rounded focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="form-group">
                    <label for="tax" class="text-green-700 font-medium">Tax:</label>
                    <input id="tax" type="text" value="{data['tax']}"
                           class="w-full p-2 border rounded focus:ring-2 focus:ring-green-300"/>
                </div>

                <div class="form-group">
                    <label for="total" class="text-green-700 font-medium">Total:</label>
                    <input id="total" type="text" value="{data['total']}"
                           class="w-full p-2 border rounded focus:ring-2 focus:ring-green-300"/>
                </div>
            </div>

            <div class="form-group">
                <label for="category" class="text-green-700 font-medium">Category:</label>
                <input id="category" type="text" value="{data['category']}"
                       class="w-full p-2 border rounded focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="form-group mt-4 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                <div class="text-yellow-800 font-medium mb-2">AI Commentary:</div>
                <p class="italic text-yellow-700">{data['commentary']}</p>
            </div>
        </div>
    </div>
    """

@app.function_name(name="form_edit")
@app.route(route="form_edit", auth_level=func.AuthLevel.ANONYMOUS)
async def form_edit(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Form edit function processing request.')

    try:
        # Get the analysis data
        response = requests.get(ANALYSIS_BLOB_URL)
        response.raise_for_status()  # Raise exception for bad status codes
        analysis_data = response.json()
        
        # Create the HTML form
        html_content = create_form_html(analysis_data)
        
        return func.HttpResponse(
            html_content,
            mimetype="text/html",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache"
            }
        )

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching analysis data: {str(e)}")
        return func.HttpResponse(
            "Error fetching analysis data",
            status_code=500
        )
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON: {str(e)}")
        return func.HttpResponse(
            "Error parsing analysis data",
            status_code=500
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            f"Unexpected error: {str(e)}",
            status_code=500
        )