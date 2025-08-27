from django import forms 

from .models import Shop, Bill, BillItem

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'owner', 'sector', 'address', 'contact_number', 'description']
        labels = {
            'name': "Shop Name",
            'owner': "Shop Owner Name",
            'sector': 'Sector',
            'address': "Shop Address",
            'contact_number': 'Contact Number', 
            'description': 'Description'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control'}),
            'sector': forms.Select(attrs={'class': 'form-control'}),  
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['customer_name', 'customer_number']
        labels = { 
            'customer_name': 'Customer Name', 
            'customer_number': 'Customer Number',
           
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_number': forms.TextInput(attrs={'class': 'form-control'}),
            
        }




  

class BillItemForm(forms.ModelForm):
    class Meta:
        model = BillItem
        fields = ['product_name', 'quantity', 'unit', 'price']
        labels = {
            'product_name': 'Product Name',
            'quantity': 'Quantity',
            'unit': 'Unit',
            'price': 'Price'
        }
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),  
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={ 
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            })
        }



class BillFilterForm(forms.Form):
    name = forms.CharField(required=False, label='Customer Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date = forms.DateField( required=False,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    label="Start Date")
    end_date = forms.DateField(required=False,widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),label="End Date")
    min_amount = forms.DecimalField(required=False,max_digits=10,decimal_places=2,widget=forms.NumberInput(attrs={'class': 'form-control'}),
    label="Minimum Amount")
    max_amount = forms.DecimalField(required=False,max_digits=10,decimal_places=2,widget=forms.NumberInput(attrs={'class': 'form-control'}),
    label="Maximum Amount") 