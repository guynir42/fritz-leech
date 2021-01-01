
# fritz-leech 

A Lightweight service to get candidates 
from a filter on the <a href="https://fritz.science/about"> ZTF Fritz marshal </a>, 
do custom analysis, and push the results 
to those sources as an annotation.

(this can be used with any SkyPortal instance)

A link to the <a href="https://skyportal.io/docs">SkyPortal documentation</a>. 

### General instructions

Before you start running this script: 
- Make sure you have a token that can read data and make annotations. 
- Store it inside a `token` file on the repo's root folder.
- Copy the `config.default.yaml` file into a `config.yaml` file. 
- Add/change the parameters in the `config.yaml` file as you see fit.
- You *must* specify the URL and the `origin` fields.
- Choose which filter ID you want to follow by setting the `filters` parameter.
  This can be an array of filter IDs. 
- If you wish to make multiple annotations from different origins, 
  please install multiple instances / folders of *fritz-leech*.
- When you feel the functions are working properly, set `upload: true` 
  in the config file to push the new annotations.

When you are done, add custom functions (as described below) 
and run the `main.py` either as a one-time script or periodically
using a chron-job. 

### Custom functions

To run your own custom code on the data in each object: 
- Add one or more files inside the `custom_functions`. 
- Each file *must* contain a function with the same name as the file. 
- That function *must* accept exactly three arguments: `obj`, `results`, `config`. 
- You can add other functions (subroutines) in that file.
- Use any data you want for each object, using the `obj` dictionary.
- Use the `config` to pass parameters to calculations.   
- The values you get from the calculation should be saved as fields in `results`. 
- The `results` dictionary is uploaded as an auto-annotation for each object. 

### Choice of candidates
You generally don't want to download all the candidates from a given filter
each time you run *fritz-leec*. 
Instead, only candidates that don't have an annotation from 
the given origin are downloaded. 

You can also add an optional `start_date` that only picks up candidates
created after this date. 
If you are interested in only the most recent candidates, 
define the `start_date` as a negative number, 
which tells *fritz-leech* to only grab candidates that many days old. 
E.g., `start_date=-5` will only get candidates from the last five days. 

### Using newer analysis versions
If you made changes in your analysis and want to upload new data
to candidates that already have an annotation from your origin, 
you can specify an `annotation_date`. 
This Arrow parsable date string tells *fritz-leech* to ignore existing
annotations that were modified *before* this date. 
So if you changed the analysis on a given date, set that as the 
`annotation_date` to make sure older candidates are updated. 
This will not update candidates older than the `start_date` in any case. 

### Using photometry/spectroscopy data

If you want to use photometry or spectra associated with a source, 
set the appropriate flags in the `config.yaml` file. 
The data will be appended to the `obj` dictionary. 

We will soon add functions to parse the JSON style data 
into numpy arrays for easier calculations. 