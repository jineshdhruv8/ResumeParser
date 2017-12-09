# Instant Resume Evaluation Engine
With the emergence of Job portal's like Linked-In, Indeed, Zip-Recruiter, Hire, etc. , job searching has become more convenient. The portals allow the job seeker to find all relevant jobs at one place. The job portals provide job seekers with easy-apply, apply via link \& email to the recruiter type of facilities. These enable the job seeker to apply for many jobs in quick time which resulted in getting many applications for a single job posting. The companies shortlist candidates by parsing their resumes to match with job-specific criteria. The companies find it difficult to parse \& extract the candidate's information due to the presence of different resume structures. Only those candidates get shortlisted whose resume is correctly parsed \& which satisfy the job-specific criteria. Further, The job seekers fail to understand why their resume not getting shortlisted. Also, job seekers find it hard to identify whether the resume has all keywords (i.e. skills, experience, qualification, etc.) \& does it meet the job description criteria which could be due to the content or format of the resume. This project focuses on extracting candidate information from its resume which is in PDF format. A Hybrid technique was used content-based & layout-based techniques for resume parsing. The hybrid approach uses a blend of rule-based and segmentation-based techniques for effective resume parsing.


## Dependency Tools & Technology
```Meteor, Python 2.7, Anaconda, PyCharm IDE```

## Dependency Package:
```pdfminer, bson, gridfs, datefinder, fuzzywuzzy, nltk, pymongo```

## Installation
Cloning the repository:
```sh
git clone https://github.com/jineshdhruv8/ResumeParser.git
```
To install Meteor in OS X & Linux:
```sh
curl https://install.meteor.com/ | sh
```
To install Meteor in Windows:
```sh
choco install meteor
```
To setup Meteor, go to "ResumeParser/resume-parser" directory and run all the below command sequentially:
```sh
meteor npm install --save babel-runtime
```
```sh
meteor npm install --save core-js
```
```sh
meteor add session
```
```sh
meteor remove autopublish
```
```sh
meteor
```
Now the App will be running at: http://localhost:3000/
```
Don't close the terminal and open new terminal to install python dependencies
```
After installing anaconda and  Python 2.7, install all dependencies
```sh
conda install -c conda-forge pdfminer 
```

```sh
conda install -c conda-forge bson 
```

```sh
pip install datefinder
```

```sh
pip install fuzzywuzzy
```

```sh
pip install -U nltk
```
```sh
python -m pip install pymongo
```
## Running the program

Now goto /Code/ResumeParser directory and run below command to insert sample resume files to database
```sh
python insert_pdf.py
```

After this step, resume files will be inserted into meteor MongoDB database and unique identifier to access these files will be stored in keys.csv file. To parse the resumes, run the following command:
```sh
python parser.py
```

## Built With:
* [MeteorJS](http://docs.meteor.com/#/full/) - web framework
* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE

## Author:
* [Jinesh Dhruv](https://github.com/jineshdhruv8)

## Acknowledgement:

* Prof. Christopher M. Homan (Rochester Institute of Technology)


