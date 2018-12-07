import boto3

polly_client = boto3.Session(
                aws_access_key_id="",
    aws_secret_access_key="",
    region_name='us-west-2').client('polly')

voiceConfig = '<speak><prosody pitch="x-high">set white with b too soon..</prosody></speak>'

response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3',
                Text = voiceConfig,
                TextType = 'ssml')

file = open('highpitch.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()
