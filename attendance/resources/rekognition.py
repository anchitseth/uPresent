import boto3
from flask import current_app
from resources.vault import obtain_data


def compare_faces_rekognition(targetId, sourceId):
    secrets = obtain_data()
    client = boto3.client('rekognition',
                          aws_access_key_id=secrets['aws_access_key_id'],
                          aws_secret_access_key=secrets['aws_secret_access_key'],
                          region_name='us-west-2')

    imageSource = open(current_app.config['UPLOAD_DIR']+sourceId, 'rb')
    imageTarget = open(current_app.config['UPLOAD_DIR']+targetId, 'rb')
    response = client.compare_faces(SimilarityThreshold=current_app.config['THRESHOLD_CONFIDENCE'],
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})
    similarity = '0'
    for faceMatch in response['FaceMatches']:
        similarity = str(faceMatch['Similarity'])
    imageSource.close()
    imageTarget.close()
    if similarity == '0':
        raise Exception('Image mismatch found!')
