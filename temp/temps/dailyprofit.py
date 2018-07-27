from temp.models import *
import temp.views
import django
from django.utils import timezone
from datetime import timedelta

twelve_hours = timezone.now() - timezone.timedelta(hours=12)
	
## SHA-256
def sha256():
	sha256List = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "SHA-256":
                        sha256List.append(pow)
	return sha256List


## X11
def x11():
	x11List = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "X11":
                        x11List.append(pow)
	return x11List
		

## Myr-Groestl
def myrGroestl():
	myrGroestlList = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Myr-Groestl":
                        myrGroestlList.append(pow)
	return myrGroestlList
		

## Qubit
def qubit():
	qubitList = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Qubit":
                        qubitList.append(pow)
	return qubitList

		
## Scrypt
def scrypt():
	scryptList = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Scrypt":
                        scryptList.append(pow)
	return scryptList
		

## Blake (14r)
def blake14r():
	blake14rList = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Blake (14r)":
                        blake14rList.append(pow)
	return blake14rList
		

## Blake (2b)
def blake2b():
	blake2bList = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Blake (2b)":
                        blake2bList.append(pow)
	return blake2bList
		

## Ethash / Dagger Hashimoto
def Ethash():
	EthashList = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Ethash":
                        EthashList.append(pow)
	return EthashList
		
		
## Skein
def skein():
	skeinList = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Skein":
                        skeinList.append(pow)
	return skeinList
		

## CryptoNightLiteV1
def cNLv1():
	cNLv1List = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "CryptoNightLiteV1":
                        cNLv1List.append(pow)
	return cNLv1List
	

## CryptoNightv7   
def cNv7(): 
	cNv7List = []
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now()) 
        for pow in diffModel:
                if pow.algo == "CryptoNightV7":
                        cNv7List.append(pow)
	return cNv7List
		

## Equihash
def equihash():
	equihashList = [] 
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Equihash":    
                        equihashList.append(pow)
	return equihashList
		

## TimeTravel10            
def timeT10():
	timeT10List = [] 
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "TimeTravel10":         
                        timeT10List.append(pow)
	return timeT10List
		
		
## PHI1612
def phi1612():  
	phi1612List = [] 
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "PHI1612":         
                        phi1612List.append(pow)
	return phi1612List
		

## NeoScrypt
def neoScrypt(): 
	neoScryptList = []  
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "NeoScrypt":              
                        neoScryptList.append(pow)
	return neoScryptList
		

## Lyra2REv2     
def lyra2REv2(): 
	lyra2REv2List = []  
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Lyra2REv2":              
                        lyra2REv2List.append(pow)
	return lyra2REv2List
		

## LBRY 
def lbry():
	lbryList = []  
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "LBRY":              
                        lbryList.append(pow)
	return lbryList
		

## Pascal
def pascal():  
	pascalList = []  
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Pascal":                   
                        pascalList.append(pow)  
	return pascalList
		

## X16R                  
def x16R():      
	x16RList = []   
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "X16R":                   
                        x16RList.append(pow)
	return x16RList
		

## X11Gost
def x11Gost():  
	x11GostList = []   
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "X11Gost":                     
                        x11GostList.append(pow) 
	return x11GostList
		

## PHI2
def phi2():    
	phi2List = []        
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "PHI2":                     
                        phi2List.append(pow) 
	return phi2List
		

## Quark
def quark():   
	quarkList = [] 
	diffModel = Difficulty.objects.filter(time__gte=twelve_hours, time__lt=timezone.now())
        for pow in diffModel:
                if pow.algo == "Quark":                     
                        quarkList.append(pow)
	return quarkList
