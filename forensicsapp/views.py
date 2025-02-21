from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Create your views

# Home Page

def home(request):
    return render(request,"home.html")

# Signup Page

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', False)
        last_name = request.POST.get('last_name', False)
        username = request.POST.get('username', False)
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        re_enter_password = request.POST.get('re_enter_password', False)
        if password == re_enter_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already Exist')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                print("User Successfully Created")
                return redirect('signin')
        else:
            messages.info(request,'Password Not Matching.....')
            return redirect('signup')
        return redirect('/')
    else:
        return render(request,"signup.html")
    
# Signin Page    

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('predict')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request,'signin.html')
    
    
# Prediction page

def predict(request):
    if (request.method == 'POST'):
        FlowDuration = int(request.POST.get('FlowDuration', False))
        TotFwdPkts = int(request.POST.get('TotFwdPkts', False))
        TotBwdPkts = int(request.POST.get('TotBwdPkts', False))
        TotLenFwdPkts = int(request.POST.get('TotLenFwdPkts', False))
        TotLenBwdPkts = int(request.POST.get('TotLenBwdPkts', False))
        FwdPktLenMax = int(request.POST.get('FwdPktLenMax', False))
        FwdPktLenMin = int(request.POST.get('FwdPktLenMin', False))
        BwdPktLenMax = int(request.POST.get('BwdPktLenMax', False))
        BwdPktLenMin = int(request.POST.get('BwdPktLenMin', False))
        FwdHeaderLen = int(request.POST.get('FwdHeaderLen', False))
        BwdHeaderLen = int(request.POST.get('BwdHeaderLen', False))
        SubflowFwdPkts = int(request.POST.get('SubflowFwdPkts', False))
        SubflowFwdByts = int(request.POST.get('SubflowFwdByts', False))
        SubflowBwdPkts = int(request.POST.get('SubflowBwdPkts', False))
        SubflowBwdByts = int(request.POST.get('SubflowBwdByts', False))
        df = pd.read_csv(r'static/dataset/Datasets.csv')
        X = df.drop('TargetOutput',axis=1)
        Y = df['TargetOutput']
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=1)
        model = RandomForestClassifier()
        model.fit(X_train, Y_train)
        predict = np.array([[FlowDuration,TotFwdPkts,TotBwdPkts,TotLenFwdPkts,TotLenBwdPkts,FwdPktLenMax,FwdPktLenMin ,BwdPktLenMax ,BwdPktLenMin ,FwdHeaderLen ,BwdHeaderLen ,SubflowFwdPkts ,SubflowFwdByts,SubflowBwdPkts,SubflowBwdByts]])
        predict = predict.reshape(1,-1)
        predict = model.predict(predict)
        # diagnosis = pred[0]
        if (predict == 0):
            r = "Brute_Force Attack"
        elif(predict == 1):
            r= "Port_Scan Attack "
        elif (predict == 2):
             r= "Web_Crwling  Attack"
        else:
            r = "Normal"
        messages.info(request, r)
    return render(request,'predict.html')

# Logout Page

def logout(request):
    auth.logout(request)
    return redirect('/')