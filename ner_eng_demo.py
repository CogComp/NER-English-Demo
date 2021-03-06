import cherrypy
import os
import json
import requests
import tabular
import sys


import hashlib
import cache_NER
from datetime import datetime

################################ Cache Loading ################################
# Instantiate Cache Class
cache = cache_NER.CacheNER()
        
cache_cogcomp_onto = cache.load("cogcomp_onto")
cache_cogcomp_conll = cache.load("cogcomp_conll")
cache_kairos_ner = cache.load("kairos_ner")
cache_onto_ner = cache.load("onto_ner")
cache_conll = cache.load("conll")

################################ Service Path ################################
BASE_HTML_PATH = "./html"
BASE_MULTILANG_NER_HTTP = 'http://dickens.seas.upenn.edu:4033/ner'
# BASE_MULTILANG_EDL_HTTP = 'http://macniece.seas.upenn.edu:4032/edl'

# BASE_COGCOMP_HTTP = "http://macniece.seas.upenn.edu:4001/annotate"
'''
def getBasicNER(lang,text):
    res_json = getMULTILANG_NER_BERT(lang,text)
    tokens = []
    endPositions = []
    if "tokens" in res_json:
        tokens = res_json["tokens"]
    if "sentences" in res_json:
        sentences = res_json["sentences"]
        if "sentenceEndPositions" in sentences:
            endPositions = sentences["sentenceEndPositions"]
    # print(tokens)
    return tokens, endPositions, res_json
'''
'''
def getBasicCCG(text):
    input = {"views":"TOKENS","text":text}
    res_out = requests.get(BASE_COGCOMP_HTTP, params = input)
    # print(res_out.text)
    res_json = json.loads(res_out.text)
    tokens = []
    endPositions = []
    if "tokens" in res_json:
        tokens = res_json["tokens"]
    if "sentences" in res_json:
        sentences = res_json["sentences"]
        if "sentenceEndPositions" in sentences:
            endPositions = sentences["sentenceEndPositions"]
    # print(tokens)
    return tokens, endPositions
'''
'''
def getBasics(annView):
    #input = {"views":"TOKENS","text":text}
    #res_out = requests.get(BASE_COGCOMP_HTTP, params = input)
    #res_json = json.loads(res_out.text)
    res_json = annView
    tokens = []
    endPositions = []
    if "tokens" in res_json:
        tokens = res_json["tokens"]
    if "sentences" in res_json:
        sentences = res_json["sentences"]
        if "sentenceEndPositions" in sentences:
            endPositions = sentences["sentenceEndPositions"]
    # print(tokens)
    return tokens, endPositions
'''
'''
def initView(myTabularView,lang,text):
    myTabularView.setText(text)
    # t,s = getBasicCCG(text)
    t,s,res_json = getBasicNER(lang,text)
    myTabularView.setTokens( t )
    myTabularView.setSentenceEnds( s )
    return res_json
'''
'''
    NER EXAMPLE: 
    # curl -d '{"lang" : "rus", "model" : "bert", "text" : "?? ?????????????? ???????? ?? ?????? ?? ????????????????, ???????? ????????????????. ?????????? ???????? ???????????? ???????????????? ???????? ?????????? ??????????????."}' -H "Content-Type: application/json" -X POST http://cogcomp.org/dc4033/ner/
'''
'''
def getMULTILANG_NER_BERT(lang,text):
    input = {"lang":lang,"model":"bert","text":text}
    res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
    #print('==========')
    #print(res_out.text)
    #print('----------')
    try:
        res_json = json.loads(res_out.text)
    except:
        res_json = {"tokens":[]}
    #print('==========')
    #print(res_json)
    #print('----------')
    return res_json

def getMULTILANG_NER_COGCOMP(lang,text):
    input = {"lang":lang,"model":"cogcomp","text":text}
    res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
    #print('==========')
    #print(res_out.text)
    #print('----------')
    try:
        # print(res_out.json())
        res_json = json.loads(res_out.text)
    except:
        res_json = {"text_tokens":[]}
    #print('==========')
    #print(res_json)
    #print('----------')
    return res_json
'''
'''
def get_NER_Eng(lang, text, model):
    input = {"lang":lang,"model": model,"text":text}
    res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
    try:
        res_json = json.loads(res_out.text)
    except:
        res_json = {"text_tokens":[]}
    return res_json
'''

def getMULTILANG_NER_COGCOMP_ONTO(lang,text):
    global cache_cogcomp_onto
    
    hash_value = hashlib.sha1(text.encode()).hexdigest()

    if cache.count(cache_cogcomp_onto) > 100:
        cache.write('cogcomp_onto', cache_cogcomp_onto)
        cache_cogcomp_onto = cache.load('cogcomp_onto')

    if hash_value in cache_cogcomp_onto[lang].keys():
        res_json, cache_cogcomp_onto = cache.read('cogcomp_onto', cache_cogcomp_onto, lang, hash_value)

    else:
        input = {"lang":lang,"model":"cogcomp_onto","text":text}
        res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
        try:
            res_json = json.loads(res_out.text)
        except:
            res_json = {"text_tokens":[]}

        cache_cogcomp_onto = cache.add('cogcomp_onto', cache_cogcomp_onto, lang, text, hash_value, res_json)
    return res_json

def getMULTILANG_NER_COGCOMP_CONLL(lang,text):
    global cache_cogcomp_conll
    
    hash_value = hashlib.sha1(text.encode()).hexdigest()

    if cache.count(cache_cogcomp_conll) > 100:
        cache.write('cogcomp_conll', cache_cogcomp_conll)
        cache_cogcomp_conll = cache.load('cogcomp_conll')

    if hash_value in cache_cogcomp_conll[lang].keys():
        res_json, cache_cogcomp_conll = cache.read('cogcomp_conll', cache_cogcomp_conll, lang, hash_value)

    else:
        input = {"lang":lang,"model":"cogcomp_conll","text":text}
        res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
        try:
            res_json = json.loads(res_out.text)
        except:
            res_json = {"text_tokens":[]}

        cache_cogcomp_conll = cache.add('cogcomp_conll', cache_cogcomp_conll, lang, text, hash_value, res_json)
    return res_json

def getMULTILANG_NER_KAIROS_NER(lang,text):
    global cache_kairos_ner
    
    hash_value = hashlib.sha1(text.encode()).hexdigest()

    if cache.count(cache_kairos_ner) > 100:
        cache.write('kairos_ner', cache_kairos_ner)
        cache_kairos_ner = cache.load('kairos_ner')

    if hash_value in cache_kairos_ner[lang].keys():
        res_json, cache_kairos_ner = cache.read('kairos_ner', cache_kairos_ner, lang, hash_value)

    else:
        input = {"lang":lang,"model":"kairos_ner","text":text}
        res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
        try:
            res_json = json.loads(res_out.text)
        except:
            res_json = {"text_tokens":[]}

        cache_kairos_ner = cache.add('kairos_ner', cache_kairos_ner, lang, text, hash_value, res_json)
    return res_json

def getMULTILANG_NER_ONTO_NER(lang,text):
    global cache_onto_ner
    
    hash_value = hashlib.sha1(text.encode()).hexdigest()

    if cache.count(cache_onto_ner) > 100:
        cache.write('onto_ner', cache_onto_ner)
        cache_onto_ner = cache.load('onto_ner')

    if hash_value in cache_onto_ner[lang].keys():
        res_json, cache_onto_ner = cache.read('onto_ner', cache_onto_ner, lang, hash_value)

    else:
        input = {"lang":lang,"model":"onto_ner","text":text}
        res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
        try:
            res_json = json.loads(res_out.text)
        except:
            res_json = {"text_tokens":[]}

        cache_onto_ner = cache.add('onto_ner', cache_onto_ner, lang, text, hash_value, res_json)
    return res_json

def getMULTILANG_NER_CONLL_NER(lang,text):
    global cache_conll
    
    hash_value = hashlib.sha1(text.encode()).hexdigest()

    if cache.count(cache_conll) > 100:
        cache.write('conll', cache_conll)
        cache_conll = cache.load('conll')

    if hash_value in cache_conll[lang].keys():
        res_json, cache_conll = cache.read('conll', cache_conll, lang, hash_value)

    else:
        input = {"lang":lang,"model":"conll","text":text}
        res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
        try:
            res_json = json.loads(res_out.text)
        except:
            res_json = {"text_tokens":[]}

        cache_conll = cache.add('conll', cache_conll, lang, text, hash_value, res_json)
    return res_json


'''
def processNER(myTabularView,lang,text):
    # print('>>>>>>>>>>>>>>>> processNER')
    annjson = initView(myTabularView, lang, text)
    # annjson = getMULTILANG_NER(lang,text)
    if "tokens" in annjson:
        myTabularView.setText(text)
        t,s = getBasics(annjson)
        myTabularView.setTokens( t ) # reset tokens in foreign language
        # myTabularView.setSentenceEnds( s )
        tokens = annjson["tokens"]
        if len(tokens) != len(myTabularView.getTokens()): return
        myTabularView.addSpanLabelView(annjson,"NER_CONLL","NER-Neural")
    try:
        annjson2 = getMULTILANG_NER_COGCOMP(lang,text)
        if "text_annotation" in annjson2:
            annjson2 = annjson2["text_annotation"]
            if "tokens" in annjson2:
                #print(annjson2)
                #print("-----------")
                tokens = annjson2["tokens"]
                if len(tokens) != len(myTabularView.getTokens()): return
                myTabularView.addSpanLabelView(annjson2,"NER_CONLL","NER-CogComp")
    except Exception as e:
        print("An exception occurred when runnin CogComp NER")
        print(e)
    return annjson,tokens
'''
'''
def doProcess(myTabularView, lang=None, text=None, anns=None):
    # print(">>>>>> PROCESS")
    myTabularView.reset()
    # initView(myTabularView, text) # DOES THE SENTENCE SPLITTER WORK FOR NON-ENGLISH TEXT?
    # for ann in anns:
    ann = "NER"
    nerjson = {}
    tokens = []
    # if True or ann in ["NER","EDL"]: 
    nerjson,tokens = processNER(myTabularView, lang, text)
    print("TOKENS",tokens)
    h = myTabularView.HTML()
    return h
'''
'''
def doProcessInnerNeural(lang=None, text=None, anns=None):
    av = getMULTILANG_NER_BERT(lang,text)
    tokens = av["tokens"]
    startAnns = tokens.copy()
    finalAnns = tokens.copy()
    for i in range(len(startAnns)):
        startAnns[i] = ""
    for i in range(len(finalAnns)):
        finalAnns[i] = ""
    if "views" in av:
        views = av["views"]
        for view in views:
            if view["viewName"] == "NER_CONLL":
                consts = view["viewData"][0]["constituents"]
                for const in consts:
                    start = const["start"]
                    end = const["end"]
                    startAnns[start] += '<span class="w3-border NER-Neural-'+const["label"]+'">' + '&nbsp;<b>[' + const["label"] + ']</b>&nbsp;'
                    finalAnns[end-1] += '&nbsp;</span>&nbsp;'
    h = ""
    h += '<div class="w3-panel w3-border w3-border-amber"><br>&nbsp;'
    for i in range(len(tokens)):
        h += startAnns[i] + tokens[i] + finalAnns[i] + " "
    h += '<br>&nbsp;'
    h += '</div><br>&nbsp;'
    return h

def doProcessInnerCogComp(lang=None, text=None, anns=None):
    av = getMULTILANG_NER_COGCOMP(lang,text)
    tokens = av["text_tokens"]
    startAnns = tokens.copy()
    finalAnns = tokens.copy()
    for i in range(len(startAnns)):
        startAnns[i] = ""
    for i in range(len(finalAnns)):
        finalAnns[i] = ""
    if "text_annotation" in av:
        if "views" in av["text_annotation"]:
            views = av["text_annotation"]["views"]
            for view in views:
                if view["viewName"] == "NER_CONLL":
                    consts = view["viewData"][0]["constituents"]
                    for const in consts:
                        start = const["start"]
                        end = const["end"]
                        startAnns[start] += '<span class="w3-border NER-Neural-'+const["label"]+'">' + '&nbsp;<b>[' + const["label"] + ']</b>&nbsp;'
                        finalAnns[end-1] += '&nbsp;</span>&nbsp;'
    h = ""
    h += '<div class="w3-panel w3-border w3-border-amber"><br>&nbsp;'
    for i in range(len(tokens)):
        h += startAnns[i] + tokens[i] + finalAnns[i] + " "
    h += '<br>&nbsp;'
    h += '</div><br>&nbsp;'
    return h
'''

def doProcessInnerCogComp(lang=None, text=None, anns=None, model=None):
    '''
    model:  "cogcomp_onto", "cogcomp_conll"
    '''
    if model == 'cogcomp_onto':
        av = getMULTILANG_NER_COGCOMP_ONTO(lang,text)
    if model == 'cogcomp_conll':
        av = getMULTILANG_NER_COGCOMP_CONLL(lang,text)
    #av = get_NER_Eng(lang,text,model)
    #print("!-------------------------------")
    #print(av)
    #print("!-------------------------------")
    tokens = av["text_tokens"]
    startAnns = tokens.copy()
    finalAnns = tokens.copy()
    for i in range(len(startAnns)):
        startAnns[i] = ""
    for i in range(len(finalAnns)):
        finalAnns[i] = ""
    if "text_annotation" in av:
        if "views" in av["text_annotation"]:
            views = av["text_annotation"]["views"]
            for view in views:
                if view["viewName"] == "NER_CONLL":
                    consts = view["viewData"][0]["constituents"]
                    for const in consts:
                        start = const["start"]
                        end = const["end"]
                        startAnns[start] += '<span class="w3-border NER-Neural-'+const["label"]+'">' + '&nbsp;<b>[' + const["label"] + ']</b>&nbsp;'
                        finalAnns[end-1] += '&nbsp;</span>&nbsp;'
    h = ""
    h += '<div class="w3-panel w3-border w3-border-amber"><br>&nbsp;'
    for i in range(len(tokens)):
        h += startAnns[i] + tokens[i] + finalAnns[i] + " "
    h += '<br>&nbsp;'
    h += '</div>'
    return h


def doProcessInnerNeural(lang=None, text=None, anns=None, model=None):
    '''
    model:  "kairos_ner", "onto_ner", "conll"
    '''
    if model == 'kairos_ner':
        av = getMULTILANG_NER_KAIROS_NER(lang,text)
    if model == 'onto_ner':
        av = getMULTILANG_NER_ONTO_NER(lang,text)
    if model == 'conll':
        av = getMULTILANG_NER_CONLL_NER(lang,text)
    #av = get_NER_Eng(lang,text,model)
    #print("!--------------Neural-----------------")
    #print(anns)
    #print("!--------------------------------------------")
    tokens = av["tokens"]
    startAnns = tokens.copy()
    finalAnns = tokens.copy()
    for i in range(len(startAnns)):
        startAnns[i] = ""
    for i in range(len(finalAnns)):
        finalAnns[i] = ""
    if "views" in av:
        views = av["views"]
        for view in views:
            if view["viewName"] == "NER_CONLL":
                consts = view["viewData"][0]["constituents"]
                for const in consts:
                    start = const["start"]
                    end = const["end"]
                    startAnns[start] += '<span class="w3-border NER-Neural-'+const["label"]+'">' + '&nbsp;<b>[' + const["label"] + ']</b>&nbsp;'
                    finalAnns[end-1] += '&nbsp;</span>&nbsp;'
    h = ""
    h += '<div class="w3-panel w3-border w3-border-amber"><br>&nbsp;'
    for i in range(len(tokens)):
        h += startAnns[i] + tokens[i] + finalAnns[i] + " "
    h += '<br>&nbsp;'
    h += '</div>'
    return h



class MyWebService(object):

    _myTabularView = None
    
    @cherrypy.expose
    def index(self):
        return open(BASE_HTML_PATH+'/index.php')

    def html(self):
        pass

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def info(self, **params):
        return {"status":"online"}

    @cherrypy.expose
    def halt(self, **params):
        cherrypy.engine.exit()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def view(self, text=None, lang=None, anns=None):
        input = { "lang" : None , "text" : None , "anns" : [] }
        try:
            data = cherrypy.request.json
        except:
            data = cherrypy.request.params
        if "lang" in data: input["lang"] = data["lang"]
        if "text" in data: input["text"] = data["text"]
        if "anns" in data: input["anns"] = data["anns"]
        # print(">>>>>>>>>", data["text"])
        
        html = ""
        if "conll" in data["anns"]:
            html += '<div class="subtitle">Neural: CoNLL</div>'#<br>'
            html += doProcessInnerNeural(data["lang"] , data["text"] , data["anns"], model="conll")
            html += '<div class="panel panel-info ng-scope" ng-if="curator.key"> <div class="panel-heading">Key</div> <div ng-bind-html="curator.key" class="ng-binding">  <div>  \
                    <table class="table" border="0" width="100%">  <tbody>  \
                    <tr><td class="text-right"><span class="NER-Neural-PER">PER</span><td> Person</td> <td class="text-right"><span class="NER-Neural-ORG">ORG</span></td><td> Organization</td><td class="text-right"><span class="NER-Neural-LOC">LOC</span></td><td> Location</td> <td class="text-right"><span class="NER-Neural-MISC">MISC</span></td><td> Miscellaneous</td></tr>  \
                    </tbody> </table> </div> </div> </div></div><br>'
        
        if "onto_ner" in data["anns"]:
            html += '<div class="subtitle">Neural: OntoNotes</div>'#<br>'
            html += doProcessInnerNeural(data["lang"] , data["text"] , data["anns"], model="onto_ner")
            html += '<div class="panel panel-info ng-scope" ng-if="curator.key"> <div class="panel-heading">Key</div> <div ng-bind-html="curator.key" class="ng-binding">  <div>  \
                    <table class="table" border="0" width="100%">  <tbody>  \
                    <tr><td class="text-right"><span class="NER-Neural-PER">PER</span><td> People, including fictional</td> <td class="text-right"><span class="NER-Neural-NORP">NORP</span></td><td> Nationalities or religious or political groups</td></tr>  \
                    <tr><td class="text-right"><span class="NER-Neural-GPE">GPE</span></td><td>Countries, cities, states</td>  <td class="text-right"><span class="NER-Neural-ORG">ORG</span></td><td> Companies, agencies, institutions, etc.</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-FAC">FAC</span></td><td>Buildings, airports, highways, bridges, etc.</td> <td class="text-right"><span class="NER-Neural-LOC">LOC</span></td><td> Non-GPE locations, mountain ranges, bodies of water</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-LAW">LAW</span></td><td>Named documents made into laws</td> <td class="text-right"><span class="NER-Neural-MONEY">MONEY</span></td><td> Monetary values, including unit</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-DATE">DATE</span></td><td>Absolute or relative dates or periods</td> <td class="text-right"><span class="NER-Neural-TIME">TIME</span></td><td>Times smaller than a day</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-PRODUCT">PRODUCT</span></td><td>Vehicles, weapons, foods, etc. (Not services)</td> <td class="text-right"><span class="NER-Neural-EVENT">EVENT</span></td><td> Named hurricanes, battles, wars, sports events, etc.</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-PERCENT">PERCENT</span></td><td>Percentage (including ???%???)</td> <td class="text-right"><span class="NER-Neural-QUANTITY">QUANTITY</span></td><td>Measurements, as of weight or distance</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-ORDINAL">ORDINAL</span></td><td>???first???, ???second???</td> <td class="text-right"><span class="NER-Neural-CARDINAL">CARDINAL</span></td><td>Numerals that do not fall under another type</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-WORK_OF_ART">WORK_OF_ART</span></td><td>Titles of books, songs, etc.</td> <td class="text-right"><span class="NER-Neural-LANGUAGE">LANGUAGE</span></td><td>Any named language</td></tr>\
                    </tbody> </table> </div> </div> </div></div><br>'
            
        if "cogcomp_conll" in data["anns"]:
            html += '<div class="subtitle">CogComp: CoNLL</div>'#<br>'
            html += doProcessInnerCogComp(data["lang"] , data["text"] , data["anns"], model="cogcomp_conll")
            html += '<div class="panel panel-info ng-scope" ng-if="curator.key"> <div class="panel-heading">Key</div> <div ng-bind-html="curator.key" class="ng-binding">  <div>  \
                    <table class="table" border="0" width="100%">  <tbody>  \
                    <tr><td class="text-right"><span class="NER-Neural-PER">PER</span><td> Person</td> <td class="text-right"><span class="NER-Neural-ORG">ORG</span></td><td> Organization</td><td class="text-right"><span class="NER-Neural-LOC">LOC</span></td><td> Location</td> <td class="text-right"><span class="NER-Neural-MISC">MISC</span></td><td> Miscellaneous</td></tr>  \
                    </tbody> </table> </div> </div> </div></div><br>'

        if "cogcomp_onto" in data["anns"]:
            html += '<div class="subtitle">CogComp: OntoNotes</div>'#<br>'
            html += doProcessInnerCogComp(data["lang"] , data["text"] , data["anns"], model="cogcomp_onto")
            html += '<div class="panel panel-info ng-scope" ng-if="curator.key"> <div class="panel-heading">Key</div> <div ng-bind-html="curator.key" class="ng-binding">  <div>  \
                    <table class="table" border="0" width="100%">  <tbody>  \
                    <tr><td class="text-right"><span class="NER-Neural-PER">PER</span><td> People, including fictional</td> <td class="text-right"><span class="NER-Neural-NORP">NORP</span></td><td> Nationalities or religious or political groups</td></tr>  \
                    <tr><td class="text-right"><span class="NER-Neural-GPE">GPE</span></td><td>Countries, cities, states</td>  <td class="text-right"><span class="NER-Neural-ORG">ORG</span></td><td> Companies, agencies, institutions, etc.</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-FAC">FAC</span></td><td>Buildings, airports, highways, bridges, etc.</td> <td class="text-right"><span class="NER-Neural-LOC">LOC</span></td><td> Non-GPE locations, mountain ranges, bodies of water</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-LAW">LAW</span></td><td>Named documents made into laws</td> <td class="text-right"><span class="NER-Neural-MONEY">MONEY</span></td><td> Monetary values, including unit</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-DATE">DATE</span></td><td>Absolute or relative dates or periods</td> <td class="text-right"><span class="NER-Neural-TIME">TIME</span></td><td>Times smaller than a day</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-PRODUCT">PRODUCT</span></td><td>Vehicles, weapons, foods, etc. (Not services)</td> <td class="text-right"><span class="NER-Neural-EVENT">EVENT</span></td><td> Named hurricanes, battles, wars, sports events, etc.</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-PERCENT">PERCENT</span></td><td>Percentage (including ???%???)</td> <td class="text-right"><span class="NER-Neural-QUANTITY">QUANTITY</span></td><td>Measurements, as of weight or distance</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-ORDINAL">ORDINAL</span></td><td>???first???, ???second???</td> <td class="text-right"><span class="NER-Neural-CARDINAL">CARDINAL</span></td><td>Numerals that do not fall under another type</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-WORK_OF_ART">WORK_OF_ART</span></td><td>Titles of books, songs, etc.</td> <td class="text-right"><span class="NER-Neural-LANGUAGE">LANGUAGE</span></td><td>Any named language</td></tr>\
                    </tbody> </table> </div> </div> </div></div><br>'

        if "kairos_ner" in data["anns"]:
            html += '<div class="subtitle">Neural: KAIROS</div>'#<br>'
            html += doProcessInnerNeural(data["lang"] , data["text"] , data["anns"], model="kairos_ner")
            html += '<div class="panel panel-info ng-scope" ng-if="curator.key"> <div class="panel-heading">Key</div> <div ng-bind-html="curator.key" class="ng-binding"> <div> \
                    <table class="table"> <tbody> \
                    <tr><td class="text-right"><span class="NER-Neural-ABS">ABS</span></td><td>Abstract, non-tangible artifacts such as software</td> <td class="text-right"><span class="NER-Neural-AML">AML</span></td><td> Animal, a non-human living organism which feeds on organic matter</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-BAL">BAL</span></td><td>A ballot for an election</td> <td class="text-right"><span class="NER-Neural-BOD">BOD</span></td><td> An identifiable, living part of an human\'s or animal\'s body,such as a eye, ear, neck, leg, etc</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-COM">COM</span></td><td>A tangible product or article of trade</td> <td class="text-right"><span class="NER-Neural-INF">INF</span></td><td> An information object</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-FAC">FAC</span></td><td>A functional, primarily man-made structure </td> <td class="text-right"><span class="NER-Neural-GPE">GPE</span></td><td> Geopolitical entities such as countries, provinces, states, cities, towns, etc.</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-LAW">LAW</span></td><td>Law, referendum, act, regulation, statute, ordinance, etc.</td> <td class="text-right"><span class="NER-Neural-LOC">LOC</span></td><td> Geopolitical entities such as bodies of wate etc.</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-MHI">MHI</span></td><td>Any medical condition or health issue</td> <td class="text-right"><span class="NER-Neural-MON">MON</span></td><td>A monetary payment</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-NAT">NAT</span></td><td>Valuable naturally materials or substances </td> <td class="text-right"><span class="NER-Neural-PLA">PLA</span></td><td> Plants/flora as well as edible fungi</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-ORG">ORG</span></td><td>Corporations, agencies etc.</td> <td class="text-right"><span class="NER-Neural-PER">PER</span></td><td> Person entities are limited to humans</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-PTH">PTH</span></td><td>An infectious microorganism or agent</td> <td class="text-right"><span class="NER-Neural-RES">RES</span></td><td>The results of a voting event</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-SEN">SEN</span></td><td>The judicial or court sentence in a Justice event</td> <td class="text-right"><span class="NER-Neural-SID">SID</span></td><td>The different sides of a conflict</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-TTL">TTL</span></td><td>A person???s title or job role</td> <td class="text-right"><span class="NER-Neural-VAL">VAL</span></td><td>A numerical value or non-numerical value</td></tr>\
                    <tr><td class="text-right"><span class="NER-Neural-VEH">VEH</span></td><td>A physical device primarily designed to move an object from one location to another</td> <td class="text-right"><span class="NER-Neural-WEA">WEA</span></td><td>A physical device that is primarily used as an instrument for physically harming or destroying entities</td></tr>\
                    </tbody> </table> </div> </div> </div></div>'
        
        #self._myTabularView = tabular.TabularView()
        #html = doProcess(self._myTabularView, data["lang"] , data["text"] , data["anns"])
                
        result = {"input": input, "html": html}
        return result
        
################################ Sys parameters ###############################
serviceHost = sys.argv[1]
servicePort = int(sys.argv[2])

if __name__ == '__main__':
    print ("")
    print ("Starting 'Multilang' rest service...")
    config = {'server.socket_host': serviceHost}
    cherrypy.config.update(config)
    config = {
      'global' : {
            #'server.socket_host' : 'dickens.seas.upenn.edu',
            'server.socket_host' : serviceHost,
            'server.socket_port' : servicePort,
            'cors.expose.on': True
      },
      '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())

      },
      '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': BASE_HTML_PATH
      },
      '/html' : {
        'tools.staticdir.on'    : True,
        'tools.staticdir.dir'   : BASE_HTML_PATH,
        'tools.staticdir.index' : 'index.php', #'inidex.html'
        'tools.gzip.on'         : True
      },
    }
    cherrypy.config.update(config)
    cherrypy.quickstart(MyWebService(), '/', config)

    # cache.write('cogcomp_onto', cache_cogcomp_onto)
    # cache.write('cogcomp_conll', cache_cogcomp_conll)
    # cache.write('kairos_ner', cache_kairos_ner)
    # cache.write('onto_ner', cache_onto_ner)
    # cache.write('conll', cache_conll)

