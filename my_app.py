import json
import Tree as g
from flask import Flask, render_template, request
import plotly.graph_objs as go

def print_state():
    for state1 in root.children:
        print(state1.parent.name)
        print(state1.name)


def print_tree():
    count = 0
    for state2 in root.children:
        print("----------------------------")
        print(count)
        print(state2.name)
        print(state2.children)
        count += 1


def state_dump():
    for state3 in states:
        state_node = g.County(name=state3)
        state_node.add_parent(root)
        root.add_child(state_node)


def json_dump():
    for county in countyData:
        county_node = g.County(json=county)

        if county_node.population < 5000:
            county_node.size = 'small'
        elif county_node.population > 100000:
            county_node.size = 'large'
        else:
            county_node.size = 'middle'

        if county_node.ratio_white < 50:
            county_node.minority = 'high'
        elif county_node.ratio_white > 90:
            county_node.minority = 'low'
        else:
            county_node.minority = 'medium'

        for state3 in root.children:
            if county_node.state == state3.name:
                county_node.parent = state3
                state3.add_child(county_node)


jsonOri = open("countyData.json")
countyData = json.load(jsonOri)

# create a root.
countyTest = countyData[:3000]
root = g.County(name="US")
Counties = g.Tree(root)

# read states from file.
states = []
statesTxt = open("state_data.txt")
for state in statesTxt:
    states.append(state.strip())


state_dump()
json_dump()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')


def get_results(result_sort, result_state, result_size, result_minority):
    results_html = []
    state_cache = None
    if result_state == 'ALL':
        for state5 in root.children:
            for county in state5.children:
                county_attributes = []
                if (county.size == result_size and county.minority == result_minority) or \
                        (result_size == 'sizeall' and county.minority == result_minority) or \
                        (result_minority == 'minall' and county.size == result_size) or \
                        (result_minority == 'minall' and result_size == 'sizeall'):
                    county_attributes.append(county.fip)
                    county_attributes.append(county.name)
                    county_attributes.append(county.population)
                    county_attributes.append(county.case_rate)
                    if county.vac_rate is None:
                        county_attributes.append(None)
                    else:
                        county_attributes.append(round(county.vac_rate, 2))
                    county_attributes.append(county.death_rate)
                    if county.ratio_white is None:
                        county_attributes.append(None)
                    else:
                        county_attributes.append(round(100 - county.ratio_white, 2))
                    county_attributes.append(county.ratio_poverty)
                results_html.append(county_attributes)
    else:
        for state4 in root.children:
            if result_state == state4.name:
                state_cache = state4
                break
        if state_cache is None:
            return [[], []]
        for county in state_cache.children:
            county_attributes = []
            if (county.size == result_size and county.minority == result_minority) or \
                    (result_size == 'sizeall' and county.minority == result_minority) or \
                    (result_minority == 'minall' and county.size == result_size) or \
                    (result_minority == 'minall' and result_size == 'sizeall'):
                county_attributes.append(county.fip)
                county_attributes.append(county.name)
                county_attributes.append(county.population)
                county_attributes.append(county.case_rate)
                if county.vac_rate is None:
                    county_attributes.append(None)
                else:
                    county_attributes.append(round(county.vac_rate, 2))
                county_attributes.append(county.death_rate)
                if county.ratio_white is None:
                    county_attributes.append(None)
                else:
                    county_attributes.append(round(100 - county.ratio_white, 2))
                county_attributes.append(county.ratio_poverty)
                results_html.append(county_attributes)
    
    if result_sort == 'deathrate':
        results_html = sorted(results_html, key=(lambda x: x[5] or 0), reverse=True)
    elif result_sort == 'caserate':
        results_html = sorted(results_html, key=(lambda x: x[3] or 0), reverse=True)
    else:
        results_html = sorted(results_html, key=(lambda x: x[4] or 0), reverse=True)

    return results_html


@app.route('/results', methods=['POST'])
def results():
    result_sort = request.form['type']
    result_state = request.form['state'].upper()
    result_size = request.form['size']
    result_minority = request.form['minority']
    results_html = get_results(result_sort, result_state, result_size, result_minority)

    sum_death = 0
    sum_vac = 0
    sum_case = 0
    sum_pov = 0

    count_death = 0
    count_vac = 0
    count_case = 0
    count_pov = 0
    if results_html != [[], []]:
        for county in results_html:
            if county[5] is not None:
                count_death += 1
                sum_death += county[5]
            if county[4] is not None:
                count_vac += 1
                sum_vac += county[4]
            if county[3] is not None:
                count_case += 1
                sum_case += county[3]
            if county[7] is not None:
                count_pov += 1
                sum_pov += county[7]
        x_vals = ['Vaccination Rate', 'Infection Rate', 'Death Rate', 'Poverty Rate']
        y_vals = [sum_vac/(count_vac+0.001), sum_case/(count_case+0.001), sum_death/(count_death+0.001), sum_pov/(count_pov+0.001)]
        bars_data = go.Bar(x=x_vals, y=y_vals)
        fig = go.Figure(data=bars_data)
        div = fig.to_html(full_html=False)
        return render_template('results.html', sort=result_sort, results=results_html, plot_div=div)

    else:
        x_vals = ['Vaccination Rate', 'Infection Rate', 'Death Rate', 'Poverty Rate']
        y_vals = [0, 0, 0, 0]
        bars_data = go.Bar(x=x_vals, y=y_vals)
        fig = go.Figure(data=bars_data)
        div = fig.to_html(full_html=False)
        return render_template('results.html', sort=result_sort, results=results_html, plot_div=div)


app.run(debug=True)