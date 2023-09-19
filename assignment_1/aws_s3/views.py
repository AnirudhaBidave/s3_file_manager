from . import forms
from .forms import list
from django.shortcuts import render
from django.contrib import messages
import boto3
from botocore.exceptions import ClientError


s3_client = boto3.client('s3')


#//////////////////////////////// Home page ///////////////////////////////
def home(request):
    return render(request, 'base.html')


#///////////////////////////// Create Bucket ////////////////////////////////
def create_bucket(request):
    form = forms.crud_form()
    if request.method == 'POST':
        form = forms.crud_form(request.POST)
        if form.is_valid():
            Bucket_Name =  form.cleaned_data['bucket_name']
            region = form.cleaned_data['Region']
            try:
                if region is None:
                    s3_client.create_bucket(Bucket=Bucket_Name)
                else:
                    s3_client = boto3.client('s3', region_name=region)
                    location = {'LocationConstraint': region}
                    s3_client.create_bucket(Bucket=Bucket_Name, CreateBucketConfiguration=location)
            except ClientError as e:
                messages.error(request, e)
            messages.info(request, 'Bucket Created Successfully')
    return render(request, 'index.html', {'form': form})


#////////////////////////////// List Buckets /////////////////////////////////
def list_bucket(request):
    bucket_list = list()
    bucket = [name[0] for name in bucket_list]
    return render(request, 'list.html', {'names':bucket})


#/////////////////////////////// upload file object ///////////////////////////
def upload(request):
    folders = []
    if request.method == 'POST':
        bucket_name = request.POST.get('bucket_name')
        if bucket_name is not None:
            request.session['bucket_name'] = bucket_name
            files = list_file(bucket_name)
            for name in files:
                if name.endswith('/'):
                    folders.append(name)
        folder_name = request.POST.get('folder_name')
        try: 
            file_name = request.FILES["file_name"]
        except Exception as e:
            file_name = None
        if bucket_name is None:
            bucket_name = request.session['bucket_name']
        if file_name is not None and bucket_name is not None or folder_name is not None:
            try:
                if folder_name is None:
                    s3_client.upload_fileobj(file_name, bucket_name, str(file_name))
                else:
                    s3_client.upload_fileobj(file_name, bucket_name, folder_name+str(file_name))
            except ClientError as e:
                messages.error(request, e)
            messages.info(request, 'File uploaded Successfully')
        return render(request, 'upload.html', {'folder': folders})
    bucket_list = list()
    buckets = [name[0] for name in bucket_list]
    return render(request, 'upload.html', {'bucket': buckets})


#/////////////////////////// Create Folder ///////////////////////////
def create_folder(request):
    form = forms.create_folder()
    if request.method == 'POST':
        form = forms.create_folder(request.POST)
        if form.is_valid():
            bucket_name = form.cleaned_data['bucket_name']
            folder_name = form.cleaned_data['folder_name']
            if not folder_name.endswith('/'):
                folder_name += '/'
            try:
                s3_client.put_object(Bucket= bucket_name, Key= folder_name)
            except ClientError as e:
                messages.error(request, e)
            messages.info(request, 'Folder Created Successfully')
    return render(request, 'create_folder.html', {'form': form})


#/////////////////////////// Delete Bucket Object ////////////////////////////////
def delete(request):
    form = forms.delete_file()
    if request.method == 'POST':
        form = forms.delete_file(request.POST)
        if form.is_valid():
            bucket_name = form.cleaned_data['bucket_name']
            request.session['bucket_name'] = bucket_name
            file_list = list_file(bucket_name)
            if file_list == None:
                messages.info(request, 'Bucket is empty')
        return render(request, 'delete.html', {'form': form, 'files': file_list})
    file_name = request.GET.get('file_name')
    try:
        bucket_name = request.session['bucket_name']
    except UnboundLocalError as e:
        bucket_name = None
    if file_name is not None and bucket_name is not None:
        try:
            s3_client.delete_object(Bucket= bucket_name, Key=str(file_name))
        except ClientError as e:
            messages.error(request, e)
        messages.info(request, 'File Deleted successfully')
    return render(request, 'delete.html', {'form': form})


#/////////////////////////// List Bucket Objects ////////////////////////////
def list_file(bucket_name):
    files_list = []
    s3_client = boto3.client('s3')
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
    except ClientError as e:
        print()
    if response['KeyCount'] == 0:
        return None
    else:
        for files in response['Contents']:
            files_list.append(files['Key'])
    return files_list


#////////////////////////// Delete Bucket ////////////////////////////////
def delete_bucket(request):
    form = forms.delete_bucket()
    if request.method == 'POST':
        form = forms.delete_bucket(request.POST)
        if form.is_valid():
            bucket_name = form.cleaned_data['bucket_name']
            try:
                s3_client.delete_bucket(Bucket=bucket_name)
            except ClientError as e:
                messages.error(request, e)
            messages.info(request, 'Bucket is deleted Successfully')
    return render(request, 'delete_bucket.html', {'form': form})


#/////////////////////////// Copy Object /////////////////////////////////
def copy_object(request):
    form = forms.copy_object()
    if request.method == 'POST':
        form = forms.copy_object(request.POST)
        if form.is_valid():
            bucket_name = form.cleaned_data['source_bucket']
            request.session['source_bucket'] = bucket_name
            file_list = list_file(bucket_name)
            if file_list == None:
                messages.info(request, 'Bucket is empty')
            buckets = [name[0] for name in list()]
            return render(request, 'copy_object.html', {'form': form, 'files': file_list, 'buckets': buckets})
    file_name = request.GET.get('file')
    dest_bucket = request.GET.get('dest_bucket')
    try:
        source_bucket = request.session['source_bucket']
    except UnboundLocalError as e:
        source_bucket = None
    if file_name is not None and dest_bucket is not None and source_bucket is not None:
        try:
            copy_source = {'Bucket': source_bucket,'Key': file_name}
            s3_client.copy(copy_source, dest_bucket, file_name)
        except ClientError as e:
            messages.error(request, e)
        messages.info(request, 'File copy successfully')
    return render(request, 'copy_object.html', {'form': form})


#//////////////////////// Move Objects ////////////////////////////////
def move_object(request):
    form = forms.move_object()
    if request.method == 'POST':
        form = forms.move_object(request.POST)
        if form.is_valid():
            bucket_name = form.cleaned_data['source_bucket']
            request.session['source_bucket'] = bucket_name
            file_list = list_file(bucket_name)
            if file_list == None:
                messages.info(request, 'Bucket is empty')
            buckets = [name[0] for name in list()]
            return render(request, 'move_object.html', {'form': form, 'files': file_list, 'buckets': buckets})
    file_name = request.GET.get('file')
    dest_bucket = request.GET.get('dest_bucket')
    try:
        source_bucket = request.session['source_bucket']
    except UnboundLocalError as e:
        source_bucket = None
    if file_name is not None and dest_bucket is not None and source_bucket is not None:
        try:
            copy_source = {'Bucket': source_bucket,'Key': file_name}
            s3_client.copy(copy_source, dest_bucket, file_name)
            s3_client.delete_object(Bucket=source_bucket, Key=str(file_name))
        except ClientError as e:
            messages.error(request, e)
        messages.info(request, 'File Move successfully')
    return render(request, 'move_object.html', {'form': form})
