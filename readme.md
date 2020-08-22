# Text Generation á la Jane Austen
### By Edith Johnston

## Table of Contents
1. [Objective and Project Details](#objective)  
2. [NLP](#nlp)  
3. [Text Generation](#text-generation)  
4. [Web App](#web-app)  
5. [Main Tools Used](#main-tools-used)  
6. [Deliverables](#deliverables)  

## Objective
### Text generation
The goal of this project was to use word embedding and either LSTMs or some variety of attention based neural networks to generate text in the semantic style of Jane Austen. 
### Fill in the Blank Style
I also created Fill in the Blank style product with the generated text, which replaces all proper nouns in the generated text with user input, based on the type of proper nouns (ie place, name, etc).

## NLP
### Text Cleaning
For this project, I used the text from all six of Jane Austen's published novels, available from Project Gutenberg. To clean the text data for processing, I built several functions to handle removes heading and footings, chapter titles, and extraneous punctuation (turns out Jane Austen was not only a terrible speller, but she also liked to use different punctuation tendencies for each of her books).   
The functions I built are all contained in the [Preprocessing](#python-modules) Python module.
### Proper Noun Handling
Since I wanted to replace all proper nouns according to type, I needed to not only extract all proper nouns from the text, but also sort the extracted proper nouns according to type, so that I could replace the nouns with distinct keys. Again, I built as series of functions to do so, which are contained in the [Proper Nouns](#python-modules) Python module. I also did much of this work in a Jupyter notebook, as this task required manual categorization in many places. This work is contained in the [Proper Nouns](#notebooks) Jupyter notebook.

## Text Generation
### Markov Chaining
Since text generation with neural nets is a fairly involved process, I needed to have an MVP text generator that didn't rely on me having time to fully train the neural net model. Therefore, I wrote a markov chain module, contained in the [Markov Chain](#python-modules) Python module and implemented in the [Markov Chain](#notebooks) Jupyter notebook.
### Neural Nets
My goal from the beginning of this project was to build and train a workable neural net model. After struggling with computing power for a while, I finally was able to get some models up and running on Google Colab, and was able to build a *decent* model. Sadly, however, at this point it remains outclassed by the Markov Chain script.

## Web App
This project is a little bit confusing to explain without a demonstration, so here's a couple quick demos!  
  
  
<figure class="video_container">
  <iframe src="https://drive.google.com/file/d/18GRFJiLAa5t437xa5jXaJ9OCgqjTEJQ9/view?usp=sharing" frameborder="0" allowfullscreen="true"> </iframe>
</figure>
  
  
<figure class="video_container">
  <video controls="true" allowfullscreen="true" poster="path/to/poster_image.png">
    <source src="https://www.github.com/edithalice/jane_austen_generation/app/media/app_demo.mp4" type="video/mp4">
    <source src="https://www.github.com/edithalice/jane_austen_generation/app/media/app_demo.ogg" type="video/ogg">
    <source src="https://www.github.com/edithalice/jane_austen_generation/app/media/app_demo.webm" type="video/webm">
  </video>
</figure>

  
<figure class="video_container">
  <video controls="true" allowfullscreen="true" poster="path/to/poster_image.png">
    <source src="https://www.github.com/edithalice/jane_austen_generation/app/media/app_demo2.mp4" type="video/mp4">
    <source src="https://www.github.com/edithalice/jane_austen_generation/app/media/app_demo2.ogg" type="video/ogg">
    <source src="https://www.github.com/edithalice/jane_austen_generation/app/media/app_demo2.webm" type="video/webm">
  </video>
</figure>
  
This app generates text, then for each type of proper noun that appears in the generated text, it asks the user to input a noun of that type.

## Main Tools Used
### NLP
- Python
- Jupyter Notebooks
### Text Generation
- TensorFlow
- FastText
- Word2Vec
- Gensim
- NLTK 
- Google Colab
### Web App
- Flask
- Bootleg

## Deliverables
### Notebooks
#### Main Workflow
1. [Text_Preprocessing](https://www.github.com/edithalice/jane_austen_generation/Text_Preprocessing.ipynb)
2. [Proper_Noun_Handling](https://www.github.com/edithalice/jane_austen_generation/Proper_Nouns.ipynb)
3. [Markov Chain Generation](https://www.github.com/edithalice/jane_austen_generation/Markov.ipynb)
4. [Neural Nets](https://www.github.com/edithalice/jane_austen_generation/Neural_Nets.ipynb)
#### EDA and sidetracks that weren't ultimately included in the final product
- [LSA and NMF](https://www.github.com/edithalice/jane_austen_generation/LSA_and_NMF.ipynb)
- [LDA](https://www.github.com/edithalice/jane_austen_generation/edith_johnston/LDA.ipynb)
- [Clustering](https://www.github.com/edithalice/jane_austen_generation/Clustering_TFIDF.ipynb)
- [FastText Embedding](https://www.github.com/edithalice/jane_austen_generation/FastText_Embedding.ipynb)
- [Word2Vec Embedding](https://www.github.com/edithalice/jane_austen_generation/Word2Vec_Embedding.ipynb)
- [Clustering with Embeddings](https://www.github.com/edithalice/jane_austen_generation/Clustering_FastText.ipynb)
### Python Modules
- [Preprocessing](https://www.github.com/edithalice/jane_austen_generation/preprocessing.py)
- [Proper Noun Handling](https://www.github.com/edithalice/jane_austen_generation/proper_nouns.py)
- [Markov Chaining](https://www.github.com/edithalice/jane_austen_generation/markov.py)
### Web App
- [App Folder](https://www.github.com/edithalice/jane_austen_generation/app)
- [Main Flask Module](https://www.github.com/edithalice/jane_austen_generation/app/app.py)
- [Demos](https://www.github.com/edithalice/jane_austen_generation/app/media)
### Presentation
- [Google Slides]()
- [PDF](https://www.github.com/edithalice/jane_austen_generation/presentation/pres.pdf)
- [Powerpoint](https://www.github.com/edithalice/jane_austen_generation/presentation/pres.pptx)


