import streamlit as st
from question_answering import QuestionAnswering
from lang_params import Params
import time
from datetime import datetime
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
#

def connect_to_db():
    MONGO = st.secrets["MONGO"]
    client = MongoClient(MONGO)
    db = client.corona_app_db
    # st.session_state.feedbacks = db.feedbacks
    return db #.feedbacks

option = st.radio(
     'Select Language - Dil Seçiniz',
     ('English', 'Türkçe'))
if option=="English":
    lang = "en"
elif option=="Türkçe":
    lang = "tr"    

@st.cache
def get_lang_params():
    return Params()
P = get_lang_params()

st.title(P.params[lang]["header1"])
st.write(P.params[lang]["header2"])
st.write("")



with st.form(key='my_form'):
    text_input = st.text_area(label=P.params[lang]["text_area_label"])
    submit_button_query = st.form_submit_button(label=P.params[lang]["submit_button_label"])


@st.cache(allow_output_mutation=True)
def load_models():
    qa_tr = QuestionAnswering(lang="tr")
    qa_tr.load_model()
    qa_en = QuestionAnswering(lang="en")
    qa_en.load_model()
    return qa_tr, qa_en
qa_tr, qa_en = load_models()

K = 1

if "logger" not in st.session_state:
    st.session_state.logger = {}

if submit_button_query:
    start = time.time()
    query = text_input
    st.session_state.queries = connect_to_db().queries
    now = datetime.now()
    st.session_state.logger = {
                "query": text_input,
                "lang": lang,
                "query_time" : now,
                "turnback_time" : time.time() - start,
                }
    results = st.session_state.queries.insert_one(st.session_state.logger)

    if lang=="tr":
        distances, ind, faq, faq_answers = qa_tr.get_best(query)
        print("---------------tr-------------------------------", query)
    if lang=="en":
        distances, ind, faq, faq_answers = qa_en.get_best(query)
        print("---------------en-------------------------------", query)
    
    now = datetime.now()
    st.session_state.logger = {"query" : str(query),
                                "lang" : str(lang),
                                "faq" : str(faq[ind[0]]),
                                "faq_answers" : str(faq_answers[ind[0]]),
                                "c" : float(distances[ind[0]]),
                                "answer_index" : int(ind[0]),
                                "correct_answer" : 1,
                                "query_time" : now,
                                "turnback_time" : time.time() - start,
                                }

    # for c,i in list(zip(distances[ind],  ind))[:K]:
    #     st.write(f"\n- SORU: {faq[i]} \n- CEVAP: {faq_answers[i]} \n- {c:.3f}")
    
try:
    st.write(f'\n {st.session_state.logger["faq"]} \
         \n {st.session_state.logger["faq_answers"]} ')
         
    # st.write(f'Calculation time : {st.session_state.logger["turnback_time"]:.3f} \
    #            \nSimilarity Distance {st.session_state.logger["c"]:.3f} ') 

except:
    pass

if st.checkbox(P.params[lang]["send_a_feedback"]):

    st.session_state.feedbacks = connect_to_db().feedbacks
    print(st.session_state.feedbacks)
    
    with st.form(key='result_form'):
        st.write(P.params[lang]["is_the_answer_correct"])
        feedback = st.radio(
            '',
            (P.params[lang]["feedback_yes"], P.params[lang]["feedback_no"]))
        if feedback== P.params[lang]["feedback_yes"]:
            feedback = 1
        else :
            feedback = 0
        
        correct_answer = st.text_input(P.params[lang]["correct_answer "])
        submit_button = st.form_submit_button(label=P.params[lang]["feedback_submit_button_label"])
    if submit_button:
        st.session_state.logger["feedback"]=int(feedback)
        # st.write("Sonuç :", feedback)  
        if feedback==1:
            st.write(P.params[lang]["thanks"])
            st.session_state.logger["correct_answer"] = 1
            # st.write(st.session_state.logger)

        elif feedback==0:
            st.write(P.params[lang]["thanks"])
            st.session_state.logger["correct_answer"] = str(correct_answer)
            # st.write(st.session_state.logger)
        
        try:
            results = st.session_state.feedbacks.insert_one(st.session_state.logger)
            st.session_state.id_last = st.session_state.logger["_id"]

        except:
            filter = {"_id" : ObjectId(st.session_state.id_last)}
            newvalues = { "$set": { 'correct_answer': str(st.session_state.logger["correct_answer"]) } }
            results = st.session_state.feedbacks.update_one(filter, newvalues)

st.markdown("----")
st.write(":computer:", P.params[lang]["github"])
st.write(":hospital:", P.params[lang]["source"])
st.write(":open_book:", P.params[lang]["book"]) 
    
    
    