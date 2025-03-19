from django.shortcuts import render,redirect
from autoapp.models import Stock,Supplier
from autoapp.forms import StockForm,SupplierForm
from django.db.models import Sum


# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def blank(request):
    return render(request, 'blank.html')

def newstock(request):
    if request.method == 'POST':
        name = request.POST['name']
        quantity = int(request.POST['quantity'])
        price = request.POST['price']
        product = request.POST['product']
        date = request.POST['date']

        # Check if the product already exists
        existing_stock = Stock.objects.filter(product=product, name=name).first()

        if existing_stock:
            # If the product exists, update its quantity
            existing_stock.quantity += quantity
            existing_stock.save()
        else:
            # If it's a new product, create a new stock entry
            Stock.objects.create(
                name=name,
                quantity=quantity,
                price=price,
                product=product,
                date=date
            )

        return redirect('/stocks')

    return render(request, 'newstock.html')



def stocks(request):
    allstocks=Stock.objects.all()
    return render(request, 'stocks.html', {'stock':allstocks})


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
    allsuppliers=Supplier.objects.all()
    return render(request, 'existingsupplier.html', {'supplier':allsuppliers})

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
