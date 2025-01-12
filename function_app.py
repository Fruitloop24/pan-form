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
    """Create a styled, editable form matching PanaceaPAN theme"""
    return f"""
    <div class="editable-fields bg-white p-6 rounded-lg shadow-lg">
        <h2 class="text-3xl font-bold mb-6 text-green-600">Receipt Details</h2>
        
        <div class="space-y-4">
            <div class="form-group">
                <label for="vendor" class="block text-green-700 font-medium mb-1">Vendor Name:</label>
                <input id="vendor" type="text" value="{data.get('vendor_name', 'Unknown')}" 
                       class="w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-300 focus:border-transparent"/>
            </div>

            <div class="form-group">
                <label for="address" class="block text-green-700 font-medium mb-1">Address:</label>
                <input id="address" type="text" value="{data.get('address', 'Unknown')}"
                       class="w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="form-group">
                <label for="phone" class="block text-green-700 font-medium mb-1">Phone:</label>
                <input id="phone" type="text" value="{data.get('phone', 'Unknown')}"
                       class="w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="form-group">
                <label for="date" class="block text-green-700 font-medium mb-1">Date:</label>
                <input id="date" type="date" value="{data.get('date', '2025-01-12')}"
                       class="w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="form-group">
                    <label for="tax" class="block text-green-700 font-medium mb-1">Tax:</label>
                    <input id="tax" type="text" value="{data.get('tax', '0.00')}"
                           class="w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-300"/>
                </div>

                <div class="form-group">
                    <label for="total" class="block text-green-700 font-medium mb-1">Total:</label>
                    <input id="total" type="text" value="{data.get('total', '0.00')}"
                           class="w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-300"/>
                </div>
            </div>

            <div class="form-group">
                <label for="category" class="block text-green-700 font-medium mb-1">Category:</label>
                <input id="category" type="text" value="{data.get('category', 'Unknown')}"
                       class="w-full p-2 border border-green-200 rounded-md focus:ring-2 focus:ring-green-300"/>
            </div>

            <div class="mt-6 bg-yellow-50 p-4 rounded-lg border-2 border-yellow-200 shadow-md">
                <div class="text-yellow-800 font-bold mb-2">AI Commentary:</div>
                <p class="italic text-yellow-700 text-lg leading-relaxed">
                    {data.get('commentary', 'AI is thinking of something witty to say...')}
                </p>
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
