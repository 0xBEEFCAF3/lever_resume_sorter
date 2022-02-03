# lever_resume_sorter
Sort resumes for a job posting using the lever API

## To get set up run 

#### Install required packages
`pip3 install -r requirments.txt`

#### Find your job posting id via the lever dashboard or their api
`curl -u 'API_KEY:' https://api.lever.co/v1/postings`
 
 
## To run

#### Export required api key 
`export LEVER_API_KEY=your_api_key`

#### Create traits json file
 Use <a href="https://github.com/armins88/lever_resume_sorter/blob/main/data_eng_traits.json"> Data engineer traits file </a> as a boiler plate. Values can be any arbituary interger value. 
 
 #### Run program
 
 `./main.py {posting_id} {path_to_traits_file}`
 
