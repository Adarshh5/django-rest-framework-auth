from django.shortcuts import render, redirect
from django.views import View
from .forms import ShopForm, BillForm, BillItemForm, BillFilterForm
from django.contrib import messages
from .models import Shop, Bill, BillItem
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def home(request):
    return render(request, 'billing/home.html')


def Profile(request):
    return render(request, 'billing/Profile.html')



@method_decorator(login_required, name='dispatch')
class RegisterShop(View):
    def get(self, request):
        user = request.user
       
        try:
           shop = Shop.objects.get(user=user.id)
           
        except ObjectDoesNotExist:
            form = ShopForm()
            return render(request, 'billing/RegisterShop.html', {'form': form})
        else:
            messages.info(request, "you have already added your shop ")
            return redirect('EditShopDetails')
    
    def post(self, request):
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.user = request.user
            shop.save()
            messages.success(request, 'Shop registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct  the error below.')
            return render('billing/ShopRegister.html', {'form': form})


@login_required
def EditShopDetails(request):
    shop = get_object_or_404(Shop, user=request.user)
    
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, "Shop details updated successfully!")
            return redirect('home')
        messages.error(request, "Please correct the errors below")
    else:
        form = ShopForm(instance=shop)
    
    return render(request, 'billing/EditShopDetails.html', {
        'form': form,
        'shop': shop
    })






@method_decorator(login_required, name="dispatch")
class CreateBill(View):
    def get(self, request):
        form1 = BillForm()
        form2 = BillItemForm()
        billid = request.session.get('billid')
        
        if not billid:
            context = {'form1': form1}
            return render(request, 'billing/CreateBill.html', context)
        else:
            try:
                bill = Bill.objects.get(id=billid)
                items = BillItem.objects.filter(bill=bill)
                context = {'form2': form2, 'bill': bill, 'items': items}
                return render(request, 'billing/CreateBill.html', context)
            except Bill.DoesNotExist:
                del request.session['billid'] 
                return redirect('CreateBill')

    def post(self, request):
        form1 = BillForm(request.POST)
        if form1.is_valid():
            bill = form1.save(commit=False)
            user = request.user
            try:
                shop = Shop.objects.get(user=user) 
                bill.shop = shop  
                bill.save()
                request.session['billid'] = bill.id  
                return redirect('CreateBill')
            except Shop.DoesNotExist:
                messages.error(request, "No shop found for this user.")
                return redirect('RegisterShop')
        context = {'form1': form1}
        messages.error(request, "Please correct the errors below")
        return render(request, 'billing/CreateBill.html', context)
    
@method_decorator(login_required,name="dispatch")
class AddItems(View):
    def post(self, request):
        form2 = BillItemForm(request.POST)
        if form2.is_valid():
            item = form2.save(commit=False)
            billid = request.session.get('billid')
            bill = get_object_or_404(Bill, pk=billid)
            item.bill = bill
            item.save()
            bill.update_total()
            return redirect('CreateBill')
        messages.error(request, 'enter correct data')
        return redirect('CreateBill')


@login_required
def DeleteItem(request):
    if request.method =="POST":
        item_id = request.POST.get('itemid')
        billid = request.session.get('billid')
        
        if not item_id or not billid:
            return redirect('CreateBill')
            
        try:
            bill = Bill.objects.get(id=billid)
            item = get_object_or_404(BillItem, id=item_id, bill=bill)
            item.delete()
            bill.update_total() 
        except (Bill.DoesNotExist, BillItem.DoesNotExist):
            messages.error(request, 'error item or bill are not exist ')
            pass 
        return redirect('CreateBill')


@login_required
def NewBill(request):
    request.session.pop('billid', None)
    return redirect('CreateBill')

@login_required
def ComplateDelete(request):
    id = request.session.get('billid')
    if id:
        try:
            bill = Bill.objects.get(id=id)
            Items = BillItem.objects.filter(bill=bill.id)
            for item in Items:
                item.delete()
            bill.delete()
        except Bill.DoesNotExist:
            pass 
        del request.session['billid'] 
        messages.info(request, "Bill information is completely deleted.")
    return redirect('CreateBill')


@login_required
def billinfo(request):
    if request.method == "POST":
       info  = request.POST.get('billinfo')
       id =  request.session.get('billid')
       bill = Bill.objects.get(id=id)
       bill.description = info
       bill.save()
       return redirect('CreateBill')


@method_decorator(login_required,name="dispatch")
class GetBill(View):
    def get(self, request):
        user = request.user
        try:
            shop = Shop.objects.get(user=user)
            billid = request.session.get('billid')
            if not billid:
                billid = request.GET.get('billid')
               
            bill = Bill.objects.get(id=billid)
            Billitems = BillItem.objects.filter(bill=bill)
        except ObjectDoesNotExist:
            messages.error(request, 'There is no bill')
            return redirect("CreateBill")
        context = {
            'shop': shop,
            'bill': bill,
            'Billitems':Billitems
        }
        request.session.pop('billid', None)
        return render(request, 'billing/GetBill.html', context)
    




@login_required
def ShowBill(request):
   
    request.session.pop('billid', None)
    user = request.user
    try:
        shop = Shop.objects.get(user=user)
        Bills = Bill.objects.filter(shop=shop)
    except ObjectDoesNotExist:
        messages.error(request, "first add you shop then see history")
        return redirect('RegisterShop')
    name = request.GET.get('name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')

    if name:
        Bills = Bills.filter(customer_name=name)
    if start_date:
        Bills = Bills.filter(created_at__gte=start_date)
    if end_date:
        Bills = Bills.filter(created_at__lte=end_date)
    if min_amount:
        Bills = Bills.filter(total_amount__gte=min_amount)
    if max_amount:
        Bills = Bills.filter(total_amount__lte=max_amount)
    


    
    FilterForm =BillFilterForm()
    return render(request, 'billing/ShowBill.html', {'Bills': Bills, 'FilterForm':FilterForm})