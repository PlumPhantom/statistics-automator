""" 
Formulas Used

 Mean=Exifi/Efi
 xi=(c1+c2)/2 where c1 and c2 are class

"""
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'num_columns' in request.form:
            num_columns = int(request.form['num_columns'])
            return render_template('index.html', num_columns=num_columns, answer=None, error=None, types=None)
        else:
            class_values = request.form.getlist('class')
            fi_values = request.form.getlist('fi')
    
            data = {
                "class": class_values,
                "fi": fi_values
            }
            types = {
                "individual": False,
                "continuous": False,
                "discrete": False
            }
            print(data)  # Print to console
            xi = []
            fi = list(map(int, data["fi"]))
            print(fi)
            efi = 0
            exifi = 0
            if any(i > 1 for i in fi):
                types['discrete'] = True
                types['individual'] = False
            else:
                types['discrete'] = False
                types['individual'] = True
            for i in fi:
                efi+=i
            if any("-" in i or " " in i for i in data["class"]):
                for i in data["class"]:
                    try:
                        if "-" in i or " " in i:
                            num1, num2 = map(int, i.replace("-", " ").split())
                            xi.append((num1, num2))
                    except Exception as e:
                        return render_template('index.html', num_columns=None, answer=None, error=e, types=None)
                    finally:
                        types['continuous'] = True
            else:
                for i in data["class"]:
                    try:
                        xi.append(int(i))
                    except Exception as e:
                        return render_template('index.html', num_columns=None, answer=None, error=e, types=None)

            if types['continuous']:
                for i, (c1, c2) in enumerate(xi): # gets both index aswell as item for that index (index, answer)
                    xi[i] = (c1 + c2)/2
            for i, o in zip(fi, xi):
                exifi+=(i*o)
            print(exifi,efi)
            answer = [exifi,efi,exifi/efi]

            return render_template('index.html', num_columns=None, answer=answer, error=None, types=None)
    return render_template('index.html', num_columns=None, answer=None, error=None, types=None)

if __name__ == '__main__':
    app.run(debug=True, port=21778, host="0.0.0.0")
