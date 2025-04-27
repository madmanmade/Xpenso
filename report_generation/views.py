from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from expenses.models import Expense
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import uuid
from datetime import datetime

@login_required(login_url='/authentication/login')
def index(request):
    return render(request, 'report_generation/index.html')

@login_required(login_url='/authentication/login')
def generate_report(request):
    if request.method == 'POST':
        # Get date range from request
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Generate unique report ID
        report_id = str(uuid.uuid4())
        
        # Get user's expenses within date range
        expenses = Expense.objects.filter(
            owner=request.user,
            date__range=[start_date, end_date]
        ).order_by('date')
        
        # Store report data in session
        request.session[f'report_{report_id}'] = {
            'expenses': list(expenses.values()),
            'start_date': start_date,
            'end_date': end_date,
            'generated_at': datetime.now().isoformat()
        }
        
        return JsonResponse({'report_id': report_id})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/authentication/login')
def download_report(request, report_id):
    # Get report data from session
    report_data = request.session.get(f'report_{report_id}')
    if not report_data:
        return JsonResponse({'error': 'Report not found'}, status=404)
    
    # Create PDF buffer
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Add report header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, f"Expense Report")
    p.setFont("Helvetica", 12)
    p.drawString(50, 730, f"Generated for: {request.user.username}")
    p.drawString(50, 710, f"Period: {report_data['start_date']} to {report_data['end_date']}")
    
    # Add expenses table
    y = 670
    p.drawString(50, y, "Date")
    p.drawString(150, y, "Category")
    p.drawString(250, y, "Description")
    p.drawString(450, y, "Amount")
    
    y -= 20
    total = 0
    
    for expense in report_data['expenses']:
        if y < 50:  # Start new page if near bottom
            p.showPage()
            y = 750
        
        p.drawString(50, y, expense['date'])
        p.drawString(150, y, expense['category'])
        p.drawString(250, y, expense['description'])
        p.drawString(450, y, f"${expense['amount']:.2f}")
        
        total += float(expense['amount'])
        y -= 20
    
    # Add total
    p.setFont("Helvetica-Bold", 12)
    p.drawString(350, y-20, f"Total: ${total:.2f}")
    
    p.save()
    buffer.seek(0)
    
    # Create response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expense_report_{report_id}.pdf"'
    response.write(buffer.getvalue())
    
    # Clean up session
    del request.session[f'report_{report_id}']
    
    return response
    except Exception as e:
        # Log the error
        logger.error(f"Error generating PDF report: {str(e)}")
        
        # Clean up buffer
        buffer.close()
        
        # Return error response
        messages.error(request, "An error occurred while generating the report. Please try again.")
        return redirect('dashboard')
