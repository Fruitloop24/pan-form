import azure.functions as func
import requests
import os
import logging  # Added this

app = func.FunctionApp()

@app.function_name(name="form_edit")
@app.route(route="form_edit", methods=["GET", "POST"], auth_level=func.AuthLevel.ANONYMOUS)
async def form_edit(req: func.HttpRequest) -> func.HttpResponse:
    """Downloads blob and returns it as HTML form. Allows GET for local testing."""
    try:
        # Grab the blob data
        data = requests.get(os.getenv("ANALYSIS_BLOB_URL")).json()
        
        # Make the form
        html = f"""
    <div style="background-color: #000; color: #F1F8E9; padding: 20px; border-radius: 10px; max-width: 600px; margin: auto; font-family: 'system-ui', sans-serif; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
        <h2 style="color: #4CAF50; font-size: 24px; margin-bottom: 15px; text-align: center;">Receipt Details</h2>
        
        <div style="margin-bottom: 20px;">
            <label for="vendor" style="color: #FDD835; font-weight: bold;">Vendor Name:</label>
            <input id="vendor" type="text" value="{data.get('vendor_name', 'Unknown')}" 
                   style="width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #4CAF50; border-radius: 5px; background-color: #2E7D32; color: #F1F8E9;"/>
        </div>

        <div style="margin-bottom: 20px;">
            <label for="address" style="color: #FDD835; font-weight: bold;">Address:</label>
            <input id="address" type="text" value="{data.get('address', 'Unknown')}" 
                   style="width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #4CAF50; border-radius: 5px; background-color: #2E7D32; color: #F1F8E9;"/>
        </div>

        <div style="margin-bottom: 20px;">
            <label for="phone" style="color: #FDD835; font-weight: bold;">Phone:</label>
            <input id="phone" type="text" value="{data.get('phone', 'Unknown')}" 
                   style="width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #4CAF50; border-radius: 5px; background-color: #2E7D32; color: #F1F8E9;"/>
        </div>

        <div style="margin-bottom: 20px;">
            <label for="date" style="color: #FDD835; font-weight: bold;">Date:</label>
            <input id="date" type="date" value="{data.get('date', 'Unknown')}" 
                   style="width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #4CAF50; border-radius: 5px; background-color: #2E7D32; color: #F1F8E9;"/>
        </div>

        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <div style="flex: 1;">
                <label for="tax" style="color: #FDD835; font-weight: bold;">Tax:</label>
                <input id="tax" type="text" value="{data.get('tax', '0.00')}" 
                       style="width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #4CAF50; border-radius: 5px; background-color: #2E7D32; color: #F1F8E9;"/>
            </div>
            <div style="flex: 1;">
                <label for="total" style="color: #FDD835; font-weight: bold;">Total:</label>
                <input id="total" type="text" value="{data.get('total', '0.00')}" 
                       style="width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #4CAF50; border-radius: 5px; background-color: #2E7D32; color: #F1F8E9;"/>
            </div>
        </div>

        <div style="margin-bottom: 20px;">
            <label for="category" style="color: #FDD835; font-weight: bold;">Category:</label>
            <input id="category" type="text" value="{data.get('category', 'Unknown')}" 
                   style="width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #4CAF50; border-radius: 5px; background-color: #2E7D32; color: #F1F8E9;"/>
        </div>

        <div style="background-color: #FDD835; color: #2E7D32; padding: 15px; border-radius: 5px; text-align: center; font-style: italic;">
            {data.get('commentary', 'AI is thinking of something witty to say...')}
        </div>
    </div>
    """
        
        # Return the form with headers that allow you to see it anywhere
        return func.HttpResponse(
            html,
            mimetype="text/html",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Cache-Control": "no-cache"
            }
        )
    except Exception as e:
        logging.error(f"Error in form_edit: {str(e)}")  # Added proper logging
        return func.HttpResponse(str(e), status_code=500)