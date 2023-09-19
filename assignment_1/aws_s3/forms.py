import re
from django import forms
import boto3


#///////////////////////// List of Available regions ///////////////////// 
reagions = [
    (None, 'select'),
    ('us-east-2', 'US East (Ohio)'), 
    ('us-east-1', 'US East (N. Virginia)'), 
    ('us-west-1','US West (N. California)'), 
    ('us-west-2','US West (Oregon)'),
    ('ap-south-1', 'Asia Pacific (Mumbai)'),
    ('ap-northeast-3', 'Asia Pacific (Osaka)'),
    ('ap-northeast-2', 'Asia Pacific (Seoul)'),
    ('ap-southeast-1', 'Asia Pacific (Singapore)'),
    ]


#/////////////////////////// List of S3buckets ///////////////////////
def list():
    bucket_list = []
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        bucket_list.append((bucket['Name'],bucket['Name']))
    return bucket_list


#///////////////////////// create Bucket form //////////////////
class crud_form(forms.Form):
    bucket_name = forms.CharField(max_length=100, label='Bucket Name', required=True)
    Region = forms.CharField(label='Regions', widget=forms.Select(choices=reagions), required=False)


#///////////////////////// Validation for bucket name ///////////////////
    def clean_bucket_name(self):
        bucket_name = self.cleaned_data['bucket_name']
        pattern = r"^(?=.{3,63}$)(?!^(\d+\.)+\d+$)(?!.*\.\.)(?!.*-$)(?!.*-$)[a-z0-9][a-z0-9.-]+[a-z0-9]$"
        if not re.match(pattern, bucket_name):
            raise forms.ValidationError('Enter valid Bucket Name')
        return bucket_name
    

#/////////////////////// Upload Object form ///////////////////////////
# class upload_form(forms.Form):
    # bucket_name = forms.CharField(label='Select Bucket', widget=forms.Select(choices=list()), required=True)
    # file = forms.FileField(label='Upload File', required=True)

#////////////////////// Create Folder Form /////////////////////////
class create_folder(forms.Form):
    bucket_name = forms.CharField(label='Select Bucket', widget=forms.Select(choices=list()), required=True)
    folder_name = forms.CharField(label= 'Floder Name: ', required=True)

#//////////////////////// Delete Object Form //////////////////////
class delete_file(forms.Form):
    bucket_name = forms.CharField(label='Select Bucket', widget=forms.Select(choices=list()),required=True)
    

#//////////////////////// Delete Bucket Form ////////////////////////
class delete_bucket(forms.Form):
    bucket_name = forms.CharField(label="Select Bucket", widget=forms.Select(choices=list()), required=True)


#//////////////////////// Copy Object Form //////////////////
class copy_object(forms.Form):
    source_bucket = forms.CharField(label="Select Soure Bucket", widget=forms.Select(choices=list()), required=True)


#///////////////////////// Move Object Form ///////////////////
class move_object(forms.Form):
    source_bucket = forms.CharField(label="Select Soure Bucket", widget=forms.Select(choices=list()), required=True)
