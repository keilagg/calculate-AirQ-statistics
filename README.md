# calculate-AirQ-statistics
Gets hourly air quality measurements and returns relevant yearly descriptive statistics.

### Table of Contents

1. [Installation](#installation)
2. [Objectives](#objectives)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing and Acknowledgements](#acknowledgments)

## Installation <a name="installation"></a>
All required dependencies are in the requirements.txt file. These can be installed as follows:

```
pip install -r requirements.txt
```

## Objectives <a name="objectives"></a>
This package was created to ease the Air Quality analysis process. Many governments and institutions
deliver these datasets in a variety of formats, making the comparison process long and tedious.

As we encounter datasets with air quality measurements, their required wrangling will be posted so
analysts could avoid these repetitive tasks.

## File Descriptions <a name="files"></a>
- valid_hours.py- Class used to represent valid measurements.
- airqstats.py- functions required to get relevant statistics.
- examples.ipynb- Notebook with basic examples.
- Data- sample data.

## Known issues
As for now, the code works for data delivered from the Environmental European Agency's page and 
Madrid's open data page. More institutions will follow.

## Licensing and Acknowledgements <a name="acknowledgments"></a>
The data used in this analysis was collected and published by the Spanish National Statistics Institute.



