from flask import Flask,render_template,request
from src.pipelines.prediction_pipeline import CustomData,PredictionPipeline

application = Flask(__name__)
app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods= ['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        data = CustomData(
            carat=float(request.form.get('carat')),
            depth=float(request.form.get('depth')),
            table = float(request.form.get('table')),
            x = float(request.form.get('x')),
            y = float(request.form.get('y')),
            z=float(request.form.get('z')),
            cut = str(request.form.get('cut')),
            color = str(request.form.get('color')),
            clarity=str(request.form.get('clarity'))


        )
        final_new_data = data.get_data_as_dataframe()
        predict_pipeline = PredictionPipeline()
        pred = predict_pipeline.predict(final_new_data)
        results = round(pred[0],2)

        return render_template('form.html',final_result=results)
    
if __name__ == '__main__':
    app.run(debug=True)
