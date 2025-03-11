# kexp radio play  
A data viz final project visualizing over 20 years of KEXP radio play data.

This project analyzes over 3 million rows of KEXP radio play data to explore how top hosts contribute to the discovery of new artists. It features interactive visualizations built with Python, Pandas, and Plotly.

___https://dataviz-kexp.streamlit.app___  

_Source_: This visualization is based on exploratory analysis of the KEXP playlist dataset. The original analysis and dataset usage guide can be found at this Kaggle notebook: https://www.kaggle.com/code/eric27n/kexp-fm-play-analysis  
_Sample_: This analysis is based on a 1% random sample of the full KEXP playlist dataset, which comprises 2,667,360 records. The sample ensures computational efficiency while maintaining the integrity and representativeness of the original data.  
_Last Updated_: see bottom of app page on link  

__GITHUB PROJECT STRUCTURE__  
This repository contains the following key components:

☑️ code/ ➡️ Development scripts and Jupyter notebooks  
&nbsp;&nbsp;&nbsp;&nbsp;final_dataviz_kexp.ipynb ➡️ Data visualization and analysis notebook  
☑️ dataset_assets/ ➡️ Project assets, including:  
&nbsp;&nbsp;&nbsp;&nbsp;kexp_sample.csv ➡️ Sample dataset used in the dashboard  
&nbsp;&nbsp;&nbsp;&nbsp;kexp_logo.png – Visual branding/logo for the app  
☑️ .devcontainer/ ➡️ Dev Container configuration 
☑️ .gitignore ➡️ Specifies files and folders to exclude from Git tracking  
☑️ README.md ➡️ Project overview and structure  
☑️ requirements.txt ➡️ Python dependencies required to run the dashboard  
☑️ streamlit_dashboard.py ➡️ Main Streamlit app (entry point for deployment)  

__KEXP 90.3 FM RADIO PLAY VISUALIZATIONS__  
After two quarters in the University of Chicago’s M.A. in Digital Studies program, I’ve developed a strong proficiency in using computational methods to explore the intersections of data, storytelling, and social inquiry. According to Jonathan Schwabish, “effective visualizations tell a story, guiding the viewer through the data while highlighting key insights and supporting evidence” (Schwabish 2021, 19). In an era where fact and fiction often blur along political lines, understanding how to analyze and manipulate data (in this case, using Python coding) is a crucial step towards fostering critical thinking and ensuring that data-driven narratives reflect truth rather than political manipulation. 

Since learning about data, statistics, and visualization, I’ve progressed from a surface-level understanding of computation to using Python libraries like Pandas, Plotly, and Bokeh to tell compelling, complex stories about the data underpinning the intricate details of our everyday lives. I’ve learned a lot over the past two quarters and, through this write-up, hope to share my first data visualization  project in the spirit of helping others who may be in a similar learning position. 

__HIGH-LEVEL OVERVIEW:__  
I. Python code to analyze over 3 million rows of KEXP 90.3 FM radio play data, with each row including details on shows, hosts, artists, songs, and albums played with corresponding date/time stamps.  
II. Developed a research hypothesis and applied data visualization tools to explore and answer it.  
III. Utilized the Pandas and Plotly libraries to create two key interactive visualizations supporting the hypothesis.  
IV. Iterated and adjusted workflows based on evolving technical skills, data insights, project and personal limitations- refining code efficiency, visualization clarity, and hypothesis testing: “Successful visualization design is inherently iterative, involving ongoing refinement as new insights emerge from the user testing and data exploration” (Munzer 2014, 69)  
V. Presented the findings, lessons learned, and insights gained throughout the project development and execution process. 

__EXPLORATION & FUTURE HYPOTHESIS:__  
As an avid longtime KEXP listener, I saw this dataset as an opportunity to explore intuitive questions that might be harder to answer in other forms of media where similar information isn’t as consistently collected. The first questions that came to mind centered on calculating and visualizing “top 10s” - a familiar, easily understandable format that lends itself to comparative analysis. But, in digging deeper, I wanted to think about how I could use these visualizations to answer a deeper question around contributions to the evolution of the station. While this is an exploratory data visualization project, I still wanted to think through how these visualizations could be the start of a deeper exploration or hypothesis question around the dataset.

___Lesson #1:___ _Data visualizations can stay surface-level or it can uncover deeper insights. The value is in not just the answers but the questions to push further analysis._

After thinking through interesting angles, the hypothesis, if I were to have more time, I would probably a hypothesis like:  
_The most frequently played artists on KEXP are often introduced by the same top hosts who consistently highlight emerging talent._ 

__DATA REVIEW:__  
The ‘KEXP-Playlist’ dataset was a CSV (comma-separated values) file containing approximately 3 million individual observations. As Munzner explains, large datasets present unique challenges: “Resource contraints, including computing power and memory, shape how data can be processed and visualized effectively” (Munzner 2014, 14). I experienced this firsthand what my computer struggled to process the full dataset. To overcome this limitation, I adjusted my approach by working with a smaller, representative sample, which allowed me to efficiently test my code, refine my methods, and ensure my visualizations functioned as intended before incorporating a larger portion of the dataset. 

___Lesson #2:___ _Sampling, along with being a tool for predictive statistics, can also be a method to test code, identify errors quickly, and refine workflows before scaling up._

To my benefit, the raw data was large but fairly organized. Beyond a small amount of additional code to remove NaN values and format string values to ensure computational accuracy, there was not a large amount of additional normalization needed to ensure this dataset was appropriate for analysis and visualization. 

_Example Data Details:_ 

Row Headers:
DateTime | Program Name | Host | Song | Artist | Album | Labels | Release Date | Local? | Live? | Request? | Rotation Status | Comment

Example Row:  
2001-02-06 15:00:00-08:00 (DateTime)  
The Roadhouse (Program Name)  
Larry Rose (Host)  
Your Girl (Songs)  
Blue States (Artist)  
Nothing Changes Under the Sun (Album)  
Eighteenth Street Lounge Music (Labels)  
2001-01-23 (Release Date)  
False (Local?) | False (Live?) | True (Request?) | Heavy (Rotation Status)  
(Comments)

Still, throughout the coding process, I would return to the raw data to iterate through and re-normalize aspects of the organization that were tripping up Python syntax. Examples of some normalization that came throughout the project include:

Ensuring all names were lowercased to prevent duplicate counting
Experimenting with DateTime formatting to explore the best method to assign variables to fine-grained aspects of DateTime (only calling month or day or day of the week or time, etc. 
Removing unknown and unpredictable values 

__METHODS & VISUALIZATIONS:__   
_Visualization #1, viz to support hypothesis_
To explore my hypothesis, I analyzed unique artists-host interactions across the station’s past 20 year history. My process for this analysis comprised of cleaning the dataset, removing duplicate artist-host pairings, normalizing artist and host names, and filtering out cases where there were outliers hosts skewing the data. Using Python’s Pandas library, I grouped the data by year and host, counting how many unique artist each host introduced annually and decided to focus on visualizing the top 10 hosts with the highest cumulative introductions using a stacked bar chart in Plotly Express. Each bar represents the number of new artists introduced per year, color-coded by host, making it easy to see which hosts consistently championed emerging talent. This visualization if one step in a large potential analysis towards identifying whether the null or alternative of my hypothesis were true. 

_Visualization #2, viz consistent with best practices_
The second graph was created with the goal of adhering to best practices in data visualization. To achieve this goal, I created a dynamic bubble chart. That tracked the top 10 most played artists on KEXP across time. After cleaning and normalizing the dataset, I extracted monthly play counts for each artist and calculate cumulative play totals by month. Using Pandas, I identified the top 10 artists for each month based on cumulative counts and visualized these counts using Plotly Express. An interactive time slider allowed users t observe how artists entered, exited, and maintained their position over time. The visualization was based on the historic Gapminder visualization and follows Schwabish’s principles of clarity, accessibility, and user engagement - transforming complex patterns into intuitive formats while highlighting the shape of this specific dataset.   

_Key Approaches and Considerations:_ 
“Color should not be decorative; it should be functional, guiding attention to the most important elements while ensuring accessibility for all users” (Schwabish 2021, 229).  
“Interactive visualizations transform passive viewing into active exploration, empowering users to ask and answer their own questions” (Schwabish 2021, 138). 

__OUTLOOK & LESSONS:__  
This project showed me that data visualization has the potential to be more than presenting numbers - it’s about crafting narratives to explore deeper insights. While the initial goal can start off straightforward, the process often reveals the importance of iterative design and coding, which can tell a richer story. Looking back, there are a few things I would approach differently. Examples include integrating GitHub for version control, which would have saved me time when I accidentally deleted important code after experimenting with small changes. Additionally, while my skills grew tremendously throughout the development of this project and my program, I now know where my skills can continue to develop including focusing on the interactivity of visual elements and fine-tuning the small details like hover text for a more engaging user experience. These lessons have not only refined my technical practices but also deepened my understanding of data visualization and the importance of documenting the process for large-scale/complex data projects. Attached below you will find a list of outlooks and lessons learned for my next data project: 

Do-overs: Use of GitHub earlier for version control  
Do-overs: Use of cloud and supercomputing for large datasets opens new possibilities and reduces limitations  
Future Learning Objectives: Better implement more robust interactivity tools  
Future Learning Objectives: Better coding control over hover point text  
Future Learning Objectives: More intuitive display the role sampling plays in this visualization and analysis  
Future Learning Objectives: Cloud and supercomputing  
Future Learning Objectives: Readability on mobile devices (the output is small on a cell phone)  
Future Learning Objectives: Creating an experience for users emphasizing higher speed use of the front-end app

__LINKS & RESOURCES:__

GitHub Profile: https://github.com/HiRickyReyes  
GitHub Project Space: https://github.com/HiRickyReyes/kexpradioplay  
Dataset: https://www.kaggle.com/datasets/eric27n/kexp-fm-song-plays  

_Resources Used:_  
Python Version: 3.12.6  
Packages: Pandas, Plotly (figure_factory, express, offline), time  

_In Text Citations:_  
Tamara Munzer, Visualization Analysis and Design (Boca Raton: CRC Press, 2014).  
Jonathan Schwabish, Better Data Visualizations: A Guide for Scholars, Researchers, and Wonks (New York: Columbia University Press, 2021).  

__📬 CONTACT__  

Project by Ricky Reyes (hirickyreyes@gmail.com)


