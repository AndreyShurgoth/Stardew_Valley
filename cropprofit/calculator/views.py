# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import CropForm
from .parameters import PARAMETERS

def crop_profit(request):
    context = {}
    profit = None
    culture_info = None

    if request.method == "POST":
        form = CropForm(request.POST)

        season = form.data.get('season', 'spring')  
        

        form.update_culture_choices(season)

        if form.is_valid():
            season = form.cleaned_data['season']
            culture = form.cleaned_data['culture']
            number_of_beds = form.cleaned_data['number_of_beds']

            culture_data = PARAMETERS.get(season, {}).get(culture)
            if culture_data:
                purchase_price = culture_data['purchase_price']
                P1 = culture_data['Prod1']
                P2 = culture_data['Prod2']
                P3 = culture_data['Prod3']
                P4 = culture_data['Prod4']
                C_K = culture_data['crop_kilkist']
                K_P = culture_data['k_posadku']
                I_B = culture_data['index_bochonok']
                income = (P1 * C_K * number_of_beds) - (number_of_beds * purchase_price)
                profit_kadka = ((P1 * 2 + 50) * number_of_beds) - (number_of_beds * purchase_price)
                profit_bochonok = (P1 * I_B * number_of_beds) - (number_of_beds * purchase_price)
                zakupka_zagal = (purchase_price * number_of_beds)
                profit = f"Ваш прибуток: {income} грн"
                culture_info = {
                    'culture': culture.capitalize(),
                    'purchase_price': purchase_price,
                    'P1': P1,
                    'P2': P2,
                    'P3': P3,
                    'P4': P4,
                    'C_K': C_K,
                    'K_P': K_P,
                    'profit_kadka': profit_kadka,
                    'profit_bochonok': profit_bochonok,
                    'income': income,
                    'zakupka_zagal': zakupka_zagal,
                    'number_of_beds': number_of_beds,
                }
    else:
        form = CropForm()

    season = request.POST.get('season', 'spring')
    form.update_culture_choices(season)

    context['form'] = form
    context['profit'] = profit
    context['culture_info'] = culture_info

    return render(request, 'crop_profit.html', context)

def update_cultures(request):
    season = request.GET.get('season')
    form = CropForm()
    form.update_culture_choices(season)
    
    culture_choices = form.fields['culture'].choices
    cultures = [culture[0] for culture in culture_choices]
    
    return JsonResponse({'cultures': cultures})
