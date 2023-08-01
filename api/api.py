from flask import Flask, request, jsonify, send_file,Response,render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired
import requests
import json
import secrets
import sys
import os
import io
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)


from utils.logger import Logger
from utils.convertToModel import ConvertToModel
from utils.convertToGeoJSON import ConvertToGeoJSON
import pandas as pd
import uuid
from sequencer import NetworkSequencer

app = Flask(__name__)
secretToken = secrets.token_hex(32)
print(secretToken)
app.config['SECRET_KEY'] =  secretToken

isDebug = False
logger = Logger()

class FormSequence(FlaskForm):
    input_feeder = StringField('Alimentador', validators=[DataRequired()])
    input_csv = FileField('Arquivo', validators=[DataRequired()])

class FormAnalisy(FlaskForm):
    input_csv_analisy = FileField('Arquivo2', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FormSequence()
    form2 = FormAnalisy()     
    if request.method == 'POST':                
        if 'sequence_submit' in request.form:
            if form.validate_on_submit():
                input_feeder = form.input_feeder.data
                input_csv = form.input_csv.data
                return upload_file(input_feeder, input_csv)
        
        
        if 'analisy_submit' in request.form:            
            print('oi')
            input_csv = form2.input_csv_analisy.data            
            df = pd.read_csv(input_csv)
            disconected = df[df["order"] == 0].shape[0]
            conected = df[df["order"] > 0].shape[0]
            erros = df[df["hasPhaseError"] == True].shape[0]
            df = df.fillna('')
            df_json = df.to_dict(orient='records') 
            with open('config.json', 'r') as arquivo:            
                config = json.load(arquivo)
            
            geojson = ConvertToGeoJSON().convert(ConvertToModel.DictionaryListToListElement(df_json),config)            
            data = {
                "connecteds": conected,
                "disconnected": disconected,
                "errors": erros                
            }
            data.update(geojson)
        
            return render_template('summary.html', data_json=data)

    return render_template('index.html', form=form,form2=form2)

def upload_file(input_feeder, input_csv):    
    api_url = f"{request.host_url.rstrip('/')}/sequence_csv"
    print(api_url)
    data = {'input_feeder': input_feeder, 'input_csv':input_csv}    

    # Arquivos para enviar na solicitação POST
    files = {
        'file': (input_csv.filename, input_csv.read(), input_csv.content_type)
    }
    try:
        response = requests.post(api_url, data=data, files=files)

        if response.status_code == 200:
            print("Arquivo enviado com sucesso!")
            csv_content = io.StringIO()
            csv_content.write(response.text)
            csv_content.seek(0)            
            return send_file(
                io.BytesIO(response.content),
                as_attachment=True,                 
                mimetype='text/csv',
                download_name = "arquivo.csv"
            )
        else:
            print(f"Erro ao enviar o arquivo. Código de resposta: {response.status_code}")
            print(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Erro na solicitação: {e}")

   



@app.route('/download_oracle')
def download_oracle():
    return download('bdgdsql_oracle')

@app.route('/download_hana')
def download_hana():
    return download('bdgdsql_hana')

def download(filename):
    # Obtém o caminho completo para o arquivo de exemplo
    example_file_path = os.path.join(app.root_path, f'sample/{filename}.sql')
    print(example_file_path)
    # Lê o conteúdo do arquivo
    with open(example_file_path, 'r') as file:
        content = file.read()

    # Retorna o arquivo de texto como resposta do Flask
    return send_file(io.BytesIO(content.encode()), as_attachment=True, download_name='exemplo.sql', mimetype='text/plain')

@app.route('/sequence_csv', methods=['POST'])
def sequence_csv():    
    print('oi')
    print(request.form)
    try:              
        feeder = request.form.get('input_feeder')    
        print('aLIMENTADIOR' + feeder)  
        print(request.files)  
        input_csv = request.files['file'] 
        #input_csv = request.data.decode()
        print(input_csv)
        df = pd.read_csv(input_csv)

        elements = df.to_dict(orient='records')

        sequencer = NetworkSequencer(logger)
        networkElements = ConvertToModel.DictToListNetworkElement(elements)
        result = sequencer.execute(feeder,networkElements,True)

        # Processar o DataFrame (exemplo: multiplicar cada valor do DataFrame pelos valores da lista)
        df_processed = pd.DataFrame(list(map(lambda e: e.__dict__,result)))
        
        if(isDebug):
            filename = str(uuid.uuid4()) + '.csv'
            project_root = os.path.dirname(os.path.abspath(__file__))
            output_directory = os.path.join(project_root, 'output')
            os.makedirs(output_directory, exist_ok=True)  
            output_csv = os.path.join(output_directory, filename)
            print(output_csv)
            df_processed.to_csv(output_csv, index=False)
            # Verificar se o arquivo foi criado corretamente
            if os.path.exists(output_csv):
                return send_file(output_csv, as_attachment=True)
            else:
                return jsonify({'message': 'Erro ao criar o arquivo CSV processado!'}), 500
        else:
            csv_data = df_processed.to_csv(index=False)                
            response = Response(csv_data, content_type='text/csv')
            response.headers['Content-Disposition'] = 'attachment; filename=data.csv'
            return response
        return 

    except Exception as e:
        return jsonify({'message': f'Erro ao processar os dados: {str(e)}'}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
