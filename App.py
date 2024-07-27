from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_tax_new_regime(income):
    slabs = [
        (300000, 0.00),
        (700000, 0.05),
        (1000000, 0.10),
        (1200000, 0.15),
        (1500000, 0.20),
        (4700000, 0.30)
    ]
    deduction = 75000
    rebate_limit = 700000
    education_cess = 0.04

    income -= deduction

    if income <= rebate_limit:
        return 0

    tax = 0
    previous_slab = 0
    for slab_limit, slab_rate in slabs:
        if income > slab_limit:
            tax += (slab_limit - previous_slab) * slab_rate
            previous_slab = slab_limit
        else:
            tax += (income - previous_slab) * slab_rate
            break

    tax += tax * education_cess
    return tax

def calculate_tax_old_regime(income, tax_saving=False):
    slabs = [
        (250000, 0.00),
        (500000, 0.05),
        (1000000, 0.20),
        (17500000, 0.30)
    ]
    standard_deduction = 50000
    education_cess = 0.04

    income -= standard_deduction

    if tax_saving:
        deductions_80c = float(request.form.get("deductions_80c", 0))
        deductions_80d = float(request.form.get("deductions_80d", 0))
        home_loan_interest = float(request.form.get("home_loan_interest", 0))
        income -= min(deductions_80c, 150000)
        income -= deductions_80d
        income -= min(home_loan_interest, 200000)

    tax = 0
    previous_slab = 0
    for slab_limit, slab_rate in slabs:
        if income > slab_limit:
            tax += (slab_limit - previous_slab) * slab_rate
            previous_slab = slab_limit
        else:
            tax += (income - previous_slab) * slab_rate
            break

    tax += tax * education_cess
    return tax

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        income = float(request.form.get('income', 0))
        tax_saving = request.form.get('tax_saving') == 'yes'

        tax_new = calculate_tax_new_regime(income)
        tax_old = calculate_tax_old_regime(income, tax_saving)

        return render_template('result.html', tax_new=tax_new, tax_old=tax_old, tax_saving=tax_saving)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



