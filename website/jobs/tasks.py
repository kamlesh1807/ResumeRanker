from website.celery import app
from .models import Job , Resume
import spacy, math, logging
nlp = spacy.load("en_core_web_sm")
from django.conf import settings
from django.contrib.auth.models import User
@app.task(serializer='json')
def scoringResumes(username, jid):
    current_job = Job.objects.get(user=User.objects.get(username=username), id=jid)
    current_job.status = "SCORING"
    current_job.save()
    listofwords = getKeywords(current_job.job_description)
    words = {}
    for word in listofwords:
        w, v = get_closest_words(word)
        words.update(zip(w, v))

    score = 0

    resumes = list(Resume.objects.filter(job=current_job).values())
    for resume in resumes:
        for w, v in words.items():
            score += v * resume['resume_data'].count(w) * wordf_idf(w)
        current_resume = Resume.objects.get(job=current_job, email=resume['email'])
        current_resume.score = score
        current_resume.save()
    current_job.status = "SCORED"
    current_job.save()
    return None


def getKeywords(data):
    doc = nlp(data)
    listofwords = [chunk.text for chunk in doc.noun_chunks] + [token.lemma_ for token in doc if token.pos_ == "VERB"]
    return listofwords


def get_closest_words(word, n=3):
    try:
        '''Get n most similar words by words.'''
        # This function can easily be expanded to get similar words to phrases--
        # using sent2vec() method defined in WithWord2Vec notebook.
        word = word.lower()
        words = [word]
        similar_vals = [1]
        try:
            similar_list = settings.MODEL.most_similar(positive=[word], topn=n)
            for tupl in similar_list:
                words.append(tupl[0])
                similar_vals.append(tupl[1])
        except:
            # If word not in vocabulary return same word and 1 similarity--
            # see initialisation of words, similarities.
            pass
        return words, similar_vals
    except Exception as e:
        logging.exception("Error in method get_word_dict(): {}".format(e))


def wordf_idf(word):
    try:
        cvs = settings.CVS.set_index('Unnamed: 0')
        no_of_cvs = 80
        idf = 0
        for i in range(no_of_cvs):
            try:
                if word in cvs.loc(0)['skill'][i].split() or word in cvs.loc(0)['exp'][i].split():
                    idf += 1
            except:
                pass
        if idf == 0:
            idf = 1
        idf = math.log(no_of_cvs / idf)
        return idf
    except Exception as e:
        logging.exception("Error in Model.py in method wordf_idf(): {}".format(e))