from flask import Flask, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect
import joblib;
import sklearn;
import os;
##########################################################################


app = Flask(__name__)


imagesFolder=os.path.join('static', 'images')
app.config['UPLOAD_FOLDER']=imagesFolder



res = ""
        

@app.route("/", methods=['GET'])
def home():
    pic1=os.path.join(app.config['UPLOAD_FOLDER'], 'me.png')
    pic2=os.path.join(app.config['UPLOAD_FOLDER'], 'fly.gif')
    pic3=os.path.join(app.config['UPLOAD_FOLDER'], 'wings.png')
    return render_template('index.html', ME=pic1, FLY=pic2, WINGS=pic3)

@app.route("/index", methods=['GET'])
def welcome_home():
    return render_template('home.html')



@app.route("/predict", methods=['POST'])
def predict():
    global res
    # Using variables to store the value of the HTML form data
    if request.method=='POST':
        let=request.form
        destination=str(let['destination'])
        airlines=str(let['q24_airlines'])
        day=let['q25_dateOf[day]']
        month=let['q25_dateOf[month]']
        source=let['q27_source']
        departure_Hour=int(let['q28_departureTime[hourSelect]'])
        departure_Min=int(let['q28_departureTime[minuteSelect]'])
        arrival_Hour=int(let['q29_arrivalTime[hourSelect]'])
        arrival_Min=int(let['q29_arrivalTime[minuteSelect]'])
        total_stops=let['q30_totalStops']

        # Calculating Total Duration
        Duration_in_Min= abs((((arrival_Hour*60) +arrival_Min) - ((departure_Hour*60)+departure_Min)))
       

        # Setting value for Total Stops
        Total_Stops =total_stops
        if Total_Stops == "Non-Stop":
            Total_Stops=0
        elif Total_Stops == "1 Stop":
            Total_Stops=1
        elif Total_Stops == "2 Stops":
            Total_Stops=2
        elif Total_Stops == "3 Stops":
            Total_Stops=3
        else:
            Total_Stops=4

        #Setting values for Journey Date & Month
        Journey_Date=day
        Journey_Month=month

        #Setting values for Arrival Hour & Minutes
        Arrival_hour=arrival_Hour
        Arrival_min=arrival_Min

        #Setting values for Departure Hour & Minutes
        Dep_hour=departure_Hour
        Dep_min=departure_Min

        #Setting values for Airlines
        Airlines_Dict = {'Airline_Air_India':0,'Airline_GoAir':0,'Airline_IndiGo':0,'Airline_Jet_Airways':0,'Airline_Jet_Airways_Business':0,
        'Airline_Multiple_carriers':0,'Airline_Multiple_carriers_Premium_economy':0,'Airline_SpiceJet':0,'Airline_Trujet':0,'Airline_Vistara':0,'Airline_Vistara_Premium_economy':0}

        Airlines_Dict[airlines]=1

        #Setting values for Destination
        Destination_Dict ={'Destination_Cochin':0,'Destination_Delhi':0, 'Destination_Hyderabad':0, 'Destination_Kolkata':0 }
        Destination_Dict[destination]=1

        #Setting values for Source
        Source_Dict={'Source_Chennai':0,'Source_Delhi':0, 'Source_Kolkata':0,'Source_Mumbai' :0}
        Source_Dict[source]=1

    
        #Loading the model here
        model=joblib.load('Flight_Ticket_Prediction_Model')

        # Using the model to predict the price
        y_pred_single = model.predict([[Total_Stops,
        Journey_Month,
        Journey_Date,
        Arrival_hour,
        Arrival_min,
        Dep_hour,
        Dep_min,
        Duration_in_Min,
        Airlines_Dict['Airline_Air_India'],
        Airlines_Dict['Airline_GoAir'],
        Airlines_Dict['Airline_IndiGo'],
        Airlines_Dict['Airline_Jet_Airways'],
        Airlines_Dict['Airline_Jet_Airways_Business'],
        Airlines_Dict['Airline_Multiple_carriers'],
        Airlines_Dict['Airline_Multiple_carriers_Premium_economy'],
        Airlines_Dict['Airline_SpiceJet'],
        Airlines_Dict['Airline_Trujet'],
        Airlines_Dict['Airline_Vistara'],
        Airlines_Dict['Airline_Vistara_Premium_economy'],
        Source_Dict['Source_Chennai'],
        Source_Dict['Source_Delhi'],
        Source_Dict['Source_Kolkata'],
        Source_Dict['Source_Mumbai'],
        Destination_Dict['Destination_Cochin'],
        Destination_Dict['Destination_Delhi'],
        Destination_Dict['Destination_Hyderabad'],
        Destination_Dict['Destination_Kolkata']]])


        res=str(round((y_pred_single[0]),2))

        

        pic1=os.path.join(app.config['UPLOAD_FOLDER'], 'loading.gif')
        return  render_template('result.html', IMAGE=pic1)
    else:
        return render_template('index.html')






@app.route('/output')  
def success():  
        return render_template('output.html',predicted_price=res)

if __name__ == "__main__":  
    app.run(debug=True)  