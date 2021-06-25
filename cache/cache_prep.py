'''
This cache_prep is used to create caches for 
"cogcomp_onto", "cogcomp_conll", "kairos_ner", "onto_ner", and "conll" 
models in ner_eng_demo.py.
'''

import json
import hashlib
import requests
import sys

#--------------------- Sample Sentences ---------------------
sample_dic = {
    "eng": [
		"Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis, a clinical method for treating psychopathology through dialogue between a patient and a psychoanalyst. Freud was born to Galician Jewish parents in the Moravian town of Freiberg, in the Austrian Empire. He qualified as a doctor of medicine in 1881 at the University of Vienna. Freud lived and worked in Vienna, having set up his clinical practice there in 1886. In 1938, Freud left Austria to escape Nazi persecution. He died in exile in the United Kingdom in 1939.",
        "Barack Hussein Obama II is an American politician and attorney who served as the 44th president of the United States from 2009 to 2017. A member of the Democratic Party, Obama was the first African-American president of the United States. He previously served as a U.S. senator from Illinois from 2005 to 2008 and an Illinois state senator from 1997 to 2004.",
		"Mohandas Karamchand Gandhi was an Indian lawyer, anti-colonial nationalist, and political ethicist. He employed nonviolent resistance to lead the successful campaign for India's independence from British rule, and in turn inspired movements for civil rights and freedom across the world. The honorific Mahātmā, first applied to him in 1914 in South Africa, is now used throughout the world.",
    ]
}


#-------------------- Annontation Function --------------------

BASE_MULTILANG_NER_HTTP = 'http://dickens.seas.upenn.edu:4033/ner'

def get_NER_Eng(lang, text, model):
    input = {"lang":lang,"model":model,"text":text}
    res_out = requests.get(BASE_MULTILANG_NER_HTTP, params = input)
    try:
        res_json = json.loads(res_out.text)
    except:
        res_json = {"text_tokens":[]}
    return res_json


#-------------------- Create/Modify Cache for NER_English-----------------

if __name__ == "__main__":
    mode = sys.argv[1]

    if mode == "create":
        for model_name in ["cogcomp_onto", "cogcomp_conll", "kairos_ner", "onto_ner", "conll"]:
            cache_NER = {}
            for lang in sample_dic.keys():
                cache_NER[lang] = {}
                for text in sample_dic[lang]:
                    hash_value = hashlib.sha1(text.encode()).hexdigest()
                    if hash_value in cache_NER[lang].keys():
                        raise ValueError('COLLISION ERROR: Different text has the same hash value!')
                    else:
                        cache_NER[lang][hash_value] = {}
                        cache_NER[lang][hash_value]['text'] = text 
                        cache_NER[lang][hash_value]['res_json'] = get_NER_Eng(lang,text,model_name)

            cache_NER_json = json.dumps(cache_NER, indent=4)
            with open('./cache/cache_'+model_name+'.json', 'w') as json_file:
                json_file.write(cache_NER_json)
            print("Successfully create cache_" + model_name +"!")
    
    
