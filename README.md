# Pan Form Generation Function

## Overview
This Azure Function represents the final stage in our serverless pipeline, generating dynamic, editable HTML forms from AI-processed data. It's designed for maximum flexibility, allowing form customization, third-party integrations, and continuous processing capabilities.

## Key Features
- Dynamic HTML form generation
- Real-time editability via blob URL endpoint
- Cross-origin accessibility
- Customizable styling and structure
- Integration-ready design
- Dual-purpose blob storage strategy

## Technical Details

### Environment Variables
```
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection
ANALYSIS_BLOB_URL=url_to_analysis_json
```

### Integration Points
- **Input Source**: Reads from AI analysis blob
- **Output**: 
  - Serves live form via blob endpoint
  - Accessible through `display/current_form.html`
  - CORS-enabled for cross-domain usage

### Form Customization Options
1. **Visual Customization**
   - Modify styling directly in template
   - Adjust layout and responsive behavior
   - Customize color scheme and branding

2. **Field Customization**
   - Add/remove form fields
   - Modify field types and validation
   - Customize input formatting

3. **Integration Options**
   - Connect to QuickBooks API
   - Link with Excel or Google Sheets
   - Integrate with ERP systems
   - Add custom processing webhooks

### Power Features
- **Live URL Endpoint**: Form accessible via blob URL
- **Edit & Continue**: Make changes and process further
- **Flexible Storage**: Both display and processing capabilities
- **API Ready**: Set up webhooks for third-party services
- **Processing Pipeline**: Can trigger additional workflows

## Pipeline Integration

### Previous Stage
Receives analyzed data from:
[pan-aiopen Repository](https://github.com/Fruitloop24/pan-aiopen)

### Extension Points
- Add database connections
- Implement custom validation
- Create approval workflows
- Trigger additional processing
- Connect to any third-party API

### Data Flow Options
1. **Basic Flow**
   - Display form
   - Edit data
   - Save changes

2. **Extended Flow**
   - Display form
   - Edit data
   - Trigger validations
   - Send to third-party systems
   - Process in connected services
   - Generate reports or alerts

## Deployment Requirements
- Azure Functions Core Tools
- Python 3.9+
- Azure Storage Account with CORS enabled
- Blob container with public access for form serving

## Development and Customization

### Local Development
1. Clone the repository
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Configure local.settings.json
5. Run locally:
```bash
func start
```

### Customization Examples
1. **Add Third-Party Integration**
```python
# Example webhook trigger
if data_validated:
    requests.post(QUICKBOOKS_WEBHOOK, json=form_data)
```

2. **Custom Storage Solution**
```python
# Example database integration
async def save_to_database(form_data):
    # Your database logic here
    pass
```

3. **Extended Processing**
```python
# Example additional processing
async def trigger_workflow(form_data):
    # Your workflow logic here
    pass
```

## Security Considerations
- CORS configuration for production
- API key management for integrations
- Secure blob access patterns
- Form validation and sanitization

## Error Handling
- Blob storage operations
- Form generation errors
- Integration failures
- Comprehensive logging

## Contributing
Contributions welcome! Please read the contributing guidelines and submit pull requests for any improvements.

## License
MIT License - see LICENSE file for details