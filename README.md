[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/aslanismailgit/semantic-question-answering/corona_app.py)

# Semantic Similarity Based Question Answering


This repo contains a [streamlit](https://streamlit.io/) app designed for answering Frequently Asked Questions (FAQs) using Semantic Similarity

The basic idea is to bring up similar answers to similar questions.

[This case study](https://github.com/PacktPublishing/Mastering-Transformers/blob/main/CH07/CH07e_Semantic_Search_with_Sentence_BERT.ipynb) is taken as reference.  


Questions similarities are calculated based on [scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html) cosine distance.

You can reach the app [here](https://share.streamlit.io/aslanismailgit/semantic-question-answering/corona_app.py)