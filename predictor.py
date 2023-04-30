import boto3

# fill it for login 
aws_access_key_id = 'aws_access_key_id'
aws_secret_access_key='aws_secret_access_key'
s3_data_path = 's3_data_path'
dataset_group_arn = 'dataset_group_arn'
dataset_arn = 'dataset_arn'
bucket_name = 'bucketname'
ForecastArn='ForecastArn'

forecast = boto3.client('forecast', region_name='us-east-1', 
                    aws_access_key_id= aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

s3_data_path = s3_data_path
dataset_group_arn = dataset_group_arn
dataset_arn = dataset_arn

# Predictor model Determination

#### Create predictor - put out of comment, the one you want to make predict with ####
# autoarima_algorithm_arn = 'arn:aws:forecast:::algorithm/ARIMA'
# prophet_algorithm_arn = 'arn:aws:forecast:::algorithm/Prophet'
autoarima_algorithm_arn = 'arn:aws:forecast:::algorithm/Deep_AR_Plus'


if autoarima_algorithm_arn == 'arn:aws:forecast:::algorithm/ARIMA':
    PredictorName='arimaperdict'
elif autoarima_algorithm_arn == 'arn:aws:forecast:::algorithm/Prophet':
    PredictorName='prophetper'
elif autoarima_algorithm_arn == 'arn:aws:forecast:::algorithm/Deep_AR_Plus':
    PredictorName='Deep_AR_Plus2'


# Predictor Setting and Hyperparameters
predictor_response = forecast.create_predictor(
    PredictorName=PredictorName,
    AlgorithmArn=autoarima_algorithm_arn,
    ForecastHorizon=365,
    PerformAutoML=False,
    PerformHPO=True,
    InputDataConfig={
        'DatasetGroupArn': dataset_group_arn,
        'SupplementaryFeatures': [
            {
                'Name': 'holiday',
                'Value': 'DE'
            },
        ]
    },
    FeaturizationConfig={
        'ForecastFrequency': 'D'
    },
    EvaluationParameters={
        'NumberOfBacktestWindows': 1,
        'BackTestWindowOffset': 365
    },
    OptimizationMetric='RMSE'
)
