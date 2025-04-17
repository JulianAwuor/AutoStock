from django.shortcuts import render,redirect,get_object_or_404
from autoapp.models import Stock,Supplier,Sale,EmployeeProfile
from autoapp.forms import StockForm,SupplierForm,EmployeeRegisterForm
from django.db.models import Sum,Q,F,ExpressionWrapper,DecimalField
from django.contrib import messages
from decimal import Decimal
from django.utils.timezone import now
from datetime import timedelta,date,datetime
from django.http import JsonResponse,HttpResponse
from collections import defaultdict
from django.template.loader import render_to_string
from weasyprint import HTML
from calendar import monthrange
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    today = now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday of this week
    week_end = week_start + timedelta(days=6)  # Sunday of this week

    # Get total stock
    total_stock = sum(stock.quantity for stock in Stock.objects.all())

    # Get weekly sales
    weekly_sales = Sale.objects.filter(datesold__range=[week_start, week_end])
    weekly_revenue = sum(sale.total_sale for sale in weekly_sales)
    weekly_profit = sum(sale.profit for sale in weekly_sales)

    context = {
        "total_stock": total_stock,
        "weekly_revenue": weekly_revenue,
        "weekly_profit": weekly_profit,
        "week_start": week_start,
        "week_end": week_end,
    }
    return render(request, "index.html", context)

def register(request):
    return render(request, 'register.html')

def blank(request):
    return render(request, 'blank.html')

def newstock(request):
    if request.method == 'POST':
        name = request.POST['name']
        quantity = int(request.POST['quantity'])
        price = Decimal(request.POST['price'])  # Convert to Decimal
        buyingprice = Decimal(request.POST['buyingprice'])  # Convert to Decimal
        product = request.POST['product']
        date = request.POST['date']

        # Check if the product already exists
        stock, created = Stock.objects.get_or_create(product=product, name=name, defaults={
            'quantity': quantity,
            'price': price,
            'buyingprice': buyingprice,
            'date': date
        })

        if not created:
            # If the stock already exists, update quantity and price details
            stock.quantity += quantity
            stock.price = price
            stock.buyingprice = buyingprice
            stock.save()

        return redirect('/stocks')

    return render(request, 'newstock.html')


def stocks(request):
    query = request.GET.get('q')  # Get search input from URL
    if query:
        allstocks = Stock.objects.filter(
            Q(product__icontains=query) | Q(name__icontains=query)
        )
    else:
        allstocks = Stock.objects.all()

    paginator = Paginator(allstocks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 👇 Pass `query` to template
    return render(request, 'stocks.html', {'stock': page_obj, 'query': query})

def newsupplier(request):
    if request.method == 'POST':
        mysupplier=Supplier(
            fullname = request.POST['fullname'],
            email = request.POST['email'],
            contact = request.POST['contact'],
            productname = request.POST['productname']
        )
        mysupplier.save()
        return redirect('/existingsupplier')

    else:
        return render(request, 'newsupplier.html')

def existingsupplier(request):
    search_query = request.GET.get('search', '')  # Get the search query from the URL parameters
    if search_query:
        # Filter suppliers based on the search query for their name, product, or contact
        allsuppliers = Supplier.objects.filter(
            fullname__icontains=search_query) | Supplier.objects.filter(
            productname__icontains=search_query) | Supplier.objects.filter(
            contact__icontains=search_query)
    else:
        allsuppliers = Supplier.objects.all()

    return render(request, 'existingsupplier.html', {'supplier': allsuppliers, 'search_query': search_query})

def charts(request):
    return render(request, 'charts.html')

def forgot(request):
    return render(request, 'forgot.html')

def login(request):
    return render(request, 'login.html')



def utilitiesanimation(request):
    return render(request, 'utilitiesanimation.html')

def utilitiesborder(request):
    return render(request, 'utilitiesborder.html')

def utilitiesother(request):
    return render(request, 'utilitiesother.html')

def utilitiescolor(request):
    return render(request, 'utilitiescolor.html')

def delete(request,id):
    stocks = Stock.objects.get(id = id)
    stocks.delete()
    return redirect('/stocks')

def deletesupplier(request,id):
    suppliers = Supplier.objects.get(id = id)
    suppliers.delete()
    return redirect('/existingsupplier')




def editstock(request,id):
    editstocks =Stock.objects.get(id = id)
    return render(request, 'editstock.html', {'stock':editstocks})


def update(request,id):
    updateinfo =Stock.objects.get(id = id)
    form =StockForm(request.POST,instance = updateinfo)
    if form.is_valid():
        form.save()
        return redirect('/stocks')

    else:
        return render(request, 'editstock.html')

def editsupplier(request,id):
    editsuppliers =Supplier.objects.get(id = id)
    return render(request, 'editsupplier.html', {'supplier':editsuppliers})


def updatesupplier(request, id):
    update = Supplier.objects.get(id=id)
    form = SupplierForm(request.POST, instance=update)
    if form.is_valid():
        form.save()
        return redirect('/existingsupplier')

    else:
        return render(request, 'editsupplier.html')



def totalstock(request):
    total_per_product = Stock.objects.values('product').annotate(total_quantity=Sum('quantity'))
    grand_total = Stock.objects.aggregate(grand_total=Sum('quantity'))['grand_total'] or 0

    return render(request, 'totalstock.html', {'total_per_product': total_per_product, 'grand_total': grand_total})


def addsale(request):
    if request.method == "POST":
        product_id = request.POST.get("product")
        quantitysold = request.POST.get("quantitysold")
        sellingprice = request.POST.get("sellingprice")

        # Validate required fields
        if not product_id or not quantitysold or not sellingprice:
            messages.error(request, "All fields are required!")
            return redirect("addsale")

        try:
            quantitysold = int(quantitysold)
            sellingprice = Decimal(sellingprice)
        except ValueError:
            messages.error(request, "Invalid input! Please enter valid numbers.")
            return redirect("addsale")

        # Ensure quantity sold is positive
        if quantitysold <= 0:
            messages.error(request, "Quantity sold must be greater than zero.")
            return redirect("addsale")

        # Get the selected product
        product = get_object_or_404(Stock, id=product_id)

        # Ensure selling price is not lower than buying price
        if sellingprice < product.buyingprice:
            messages.error(request, "Selling price cannot be lower than buying price!")
            return redirect("addsale")

        # Check if there is enough stock
        if quantitysold > product.quantity:
            messages.error(request, "Not enough stock available!")
            return redirect("addsale")

        # Deduct sold quantity from stock
        product.quantity -= quantitysold
        product.save()

        # Create a sale record
        Sale.objects.create(
            product=product,
            quantitysold=quantitysold,
            sellingprice=sellingprice
        )

        messages.success(request, "Sale recorded successfully!")
        return redirect("addsale")  # Redirect to sales list page

    # Get all products for dropdown selection
    products = Stock.objects.all()
    return render(request, "addsale.html", {"products": products})


def salesummary(request):
    today = now().date()

    # Weekly range
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)  # Sunday

    # Monthly range
    month_start = today.replace(day=1)
    last_day = monthrange(today.year, today.month)[1]
    month_end = today.replace(day=last_day)

    # Queries
    daily_sales = Sale.objects.filter(datesold=today)
    weekly_sales = Sale.objects.filter(datesold__range=[week_start, week_end])
    monthly_sales = Sale.objects.filter(datesold__range=[month_start, month_end])

    # Daily calculations
    daily_revenue = sum(sale.total_sale for sale in daily_sales)
    daily_profit = sum(sale.profit for sale in daily_sales)

    # Weekly calculations
    weekly_revenue = sum(sale.total_sale for sale in weekly_sales)
    weekly_profit = sum(sale.profit for sale in weekly_sales)

    # Monthly calculations
    monthly_revenue = sum(sale.total_sale for sale in monthly_sales)
    monthly_profit = sum(sale.profit for sale in monthly_sales)

    context = {
        "daily_revenue": daily_revenue,
        "daily_profit": daily_profit,
        "weekly_revenue": weekly_revenue,
        "weekly_profit": weekly_profit,
        "monthly_revenue": monthly_revenue,
        "monthly_profit": monthly_profit,
        "today": today,
        "week_start": week_start,
        "week_end": week_end,
        "month_start": month_start,
        "month_end": month_end,
    }

    return render(request, "salesummary.html", context)

def saleslist(request):
    query = request.GET.get('q')
    if query:
        sales_queryset = Sale.objects.filter(
            Q(product__product__icontains=query)
        ).order_by('-datesold')
    else:
        sales_queryset = Sale.objects.all().order_by('-datesold')

    paginator = Paginator(sales_queryset, 10)  # Show 10 sales per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'saleslist.html', {
        'sales': page_obj,       # 👉 This should be the paginated data
        'query': query           # 👉 Optional: if you want to preserve search input in the form
    })

def weekly_sales_data(request):
    today = now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)  # Sunday

    # Filter sales within this week
    weekly_sales = Sale.objects.filter(datesold__range=[week_start, week_end])

    # Use a dictionary to sum sales per day
    sales_by_day = defaultdict(float)
    for sale in weekly_sales:
        day_name = sale.datesold.strftime("%A")  # Convert date to day name
        sales_by_day[day_name] += float(sale.total_sale)  # Ensure it's a number

    # Sort days to follow the correct order (Monday-Sunday)
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    labels = [day for day in week_days if day in sales_by_day]
    earnings = [sales_by_day[day] for day in labels]

    return JsonResponse({"labels": labels, "earnings": earnings})


def low_stock_alert(request):
    low_stock_items = Stock.objects.filter(quantity__lte=10)  # Get items with quantity ≤ 10
    data = {
        "alerts": [
            {"product": item.product, "quantity": item.quantity, "date": item.date.strftime("%Y-%m-%d")}
            for item in low_stock_items
        ]
    }
    return JsonResponse(data)




def product_tracker(request, product_id):
    product = get_object_or_404(Stock, id=product_id)

    sales = Sale.objects.filter(product=product)

    # Aggregated values
    total_quantity_sold = sales.aggregate(total=Sum("quantitysold"))["total"] or 0
    total_revenue = sum(sale.quantitysold * sale.sellingprice for sale in sales)
    total_profit = sum(sale.quantitysold * (sale.sellingprice - product.buyingprice) for sale in sales)

    # Distinct sales dates
    sales_dates = sales.values("datesold").distinct().order_by("-datesold")

    context = {
        "product": product,
        "total_quantity_sold": total_quantity_sold,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "sales_dates": sales_dates,
    }

    return render(request, "product_tracker.html", context)


def generate_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    all_sales = Sale.objects.all()

    # Date range filtering for table & pie chart
    if start_date and end_date:
        sales = all_sales.filter(datesold__range=[start_date, end_date])
        selected_start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        selected_end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        sales = all_sales.filter(datesold__month=today.month)
        selected_start_date = start_of_month
        selected_end_date = today

    # Yearly Totals (can remain for the whole year regardless of filters)
    yearly_sales = all_sales.filter(datesold__gte=start_of_year, datesold__lte=today)
    total_sales = sum(s.total_sale for s in yearly_sales)
    total_profit = sum(s.profit for s in yearly_sales)

    # Daily
    daily_sales = sales.filter(datesold=today)
    daily_units = sum(s.quantitysold for s in daily_sales)
    daily_amount = sum(s.total_sale for s in daily_sales)

    # Weekly
    weekly_sales = sales.filter(datesold__gte=start_of_week, datesold__lte=today)
    weekly_units = sum(s.quantitysold for s in weekly_sales)
    weekly_amount = sum(s.total_sale for s in weekly_sales)

    # Monthly — now dynamically based on selected date range
    monthly_sales = sales.filter(datesold__gte=selected_start_date, datesold__lte=selected_end_date)
    monthly_units = sum(s.quantitysold for s in monthly_sales)
    monthly_amount = sum(s.total_sale for s in monthly_sales)

    # Pie Chart Data
    chart_data = defaultdict(int)
    for sale in sales:
        chart_data[sale.product.product] += sale.quantitysold

    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_profit': total_profit,

        'daily_total_quantity': daily_units,
        'daily_total_amount': daily_amount,
        'weekly_total_quantity': weekly_units,
        'weekly_total_amount': weekly_amount,
        'monthly_total_quantity': monthly_units,
        'monthly_total_amount': monthly_amount,

        'chart_data': {
            'keys': list(chart_data.keys()),
            'values': list(chart_data.values())
        },
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'generate_report.html', context)


def download_report_pdf(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        chart_image = request.POST.get('chart_image')

        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_year = today.replace(month=1, day=1)

        all_sales = Sale.objects.all()

        # Validate and parse dates
        try:
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = None
            end_date = None

        # Apply date filtering
        if start_date and end_date:
            sales = all_sales.filter(datesold__range=[start_date, end_date])
        else:
            # fallback to current month
            start_of_month = today.replace(day=1)
            sales = all_sales.filter(datesold__month=today.month)
            start_date = start_of_month
            end_date = today

        yearly_sales = all_sales.filter(datesold__gte=start_of_year, datesold__lte=today)
        total_sales = sum(s.total_sale for s in yearly_sales)
        total_profit = sum(s.profit for s in yearly_sales)

        # Daily & Weekly ranges are still based on today's date
        daily_sales = sales.filter(datesold=today)
        weekly_sales = sales.filter(datesold__gte=start_of_week, datesold__lte=today)

        # ✅ Monthly — now correctly based on selected date range
        monthly_sales = sales.filter(datesold__gte=start_date, datesold__lte=end_date)

        chart_data = defaultdict(int)
        for sale in sales:
            chart_data[sale.product.product] += sale.quantitysold

        context = {
            'sales': sales,
            'total_sales': total_sales,
            'total_profit': total_profit,
            'daily_total_quantity': sum(s.quantitysold for s in daily_sales),
            'daily_total_amount': sum(s.total_sale for s in daily_sales),
            'weekly_total_quantity': sum(s.quantitysold for s in weekly_sales),
            'weekly_total_amount': sum(s.total_sale for s in weekly_sales),
            'monthly_total_quantity': sum(s.quantitysold for s in monthly_sales),
            'monthly_total_amount': sum(s.total_sale for s in monthly_sales),
            'chart_image': chart_image,
            'start_date': start_date,
            'end_date': end_date,
        }

        html_string = render_to_string('download_report_pdf.html', context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
        return response


@login_required
def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            nationalid = form.cleaned_data.get('nationalid')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')

            EmployeeProfile.objects.create(
                user=user,
                nationalid=nationalid,
                phone=phone,
                email=email,
            )

            messages.success(request, f"Employee '{user.username}' was successfully registered.")
            return redirect('register_employee')
    else:
        form = EmployeeRegisterForm()
    return render(request, 'register_employee.html', {'form': form})